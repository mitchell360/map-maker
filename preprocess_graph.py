#!/usr/bin/env python3
"""
Preprocess itiner-e roman_roads.ndjson into a compact routing graph.
Outputs: itinere_graph.json (nodes, edges, spatial index)
"""

import json
import math
from collections import defaultdict

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two coordinates."""
    R = 6371  # Earth radius in km
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def coord_to_key(lat, lon, precision=4):
    """Round coordinates to create a node key."""
    return f"{round(lat, precision)},{round(lon, precision)}"

def grid_cell(lat, lon, cell_size=0.25):
    """Get grid cell for spatial index."""
    return f"{int(lat/cell_size)},{int(lon/cell_size)}"

def main():
    print("Loading roman_roads.ndjson...")
    features = []
    with open('roman_roads.ndjson', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    feature = json.loads(line)
                    features.append(feature)
                except json.JSONDecodeError:
                    pass
    
    print(f"Loaded {len(features)} features")
    
    # Build nodes and edges
    nodes = {}  # key -> {lat, lon, id}
    edges = []  # [{from, to, length, type, coords}]
    node_id_counter = 0
    
    # Spatial index: grid cell -> list of edge indices
    spatial_index = defaultdict(list)
    
    for feature in features:
        geom = feature.get('geometry', {})
        props = feature.get('properties', {})
        
        if geom.get('type') != 'LineString':
            continue
            
        coords = geom.get('coordinates', [])
        if len(coords) < 2:
            continue
        
        segment_type = props.get('type', 'Road')
        
        # Determine edge type category
        if segment_type == 'Sea Lane':
            edge_type = 'sea'
        elif segment_type == 'River':
            edge_type = 'river'
        else:
            edge_type = 'land'
        
        # Get length from properties or calculate
        length_km = props.get('_lengthInKm')
        if not length_km:
            # Calculate from coordinates
            length_km = 0
            for i in range(len(coords) - 1):
                lon1, lat1 = coords[i]
                lon2, lat2 = coords[i+1]
                length_km += haversine_distance(lat1, lon1, lat2, lon2)
        
        # Create/get nodes for start and end points
        start_lon, start_lat = coords[0]
        end_lon, end_lat = coords[-1]
        
        start_key = coord_to_key(start_lat, start_lon)
        end_key = coord_to_key(end_lat, end_lon)
        
        if start_key not in nodes:
            nodes[start_key] = {'lat': start_lat, 'lon': start_lon, 'id': node_id_counter}
            node_id_counter += 1
        
        if end_key not in nodes:
            nodes[end_key] = {'lat': end_lat, 'lon': end_lon, 'id': node_id_counter}
            node_id_counter += 1
        
        start_id = nodes[start_key]['id']
        end_id = nodes[end_key]['id']
        
        # Skip self-loops
        if start_id == end_id:
            continue
        
        edge_idx = len(edges)
        
        # Store edge with simplified coordinate path
        edge = {
            'from': start_id,
            'to': end_id,
            'length': round(length_km, 3),
            'type': edge_type,
            'coords': [[round(c[1], 5), round(c[0], 5)] for c in coords]  # [lat, lon] format
        }
        edges.append(edge)
        
        # Add to spatial index (all cells the edge passes through)
        for coord in coords:
            lon, lat = coord
            cell = grid_cell(lat, lon)
            if edge_idx not in spatial_index[cell]:
                spatial_index[cell].append(edge_idx)
    
    print(f"Created {len(nodes)} nodes and {len(edges)} edges")
    
    # Count by type
    land_edges = sum(1 for e in edges if e['type'] == 'land')
    sea_edges = sum(1 for e in edges if e['type'] == 'sea')
    river_edges = sum(1 for e in edges if e['type'] == 'river')
    print(f"Edge types: {land_edges} land, {sea_edges} sea, {river_edges} river")
    
    # ============================================
    # ADD SYNTHETIC PORT CONNECTIONS
    # Connect sea lane endpoints to nearby land road nodes
    # This bridges the otherwise-disconnected sea and land networks
    # ============================================
    print("\nAdding synthetic port connections...")
    
    # Build node lookup by id
    nodes_by_id = {n['id']: n for n in nodes.values()}
    
    # Find sea-only and land-only nodes
    sea_node_ids = set()
    for e in edges:
        if e['type'] == 'sea':
            sea_node_ids.add(e['from'])
            sea_node_ids.add(e['to'])
    
    land_node_ids = set()
    for e in edges:
        if e['type'] != 'sea':
            land_node_ids.add(e['from'])
            land_node_ids.add(e['to'])
    
    # Nodes that have ONLY sea (not already connected to land)
    sea_only_nodes = sea_node_ids - land_node_ids
    
    # For each sea-only node, find nearest land node and add a port connection
    port_edges_added = 0
    PORT_SEARCH_RADIUS = 20  # km - max distance to search for land connection
    
    for sea_nid in sea_only_nodes:
        sea_node = nodes_by_id[sea_nid]
        sea_lat, sea_lon = sea_node['lat'], sea_node['lon']
        
        # Find nearest land node
        best_land = None
        best_dist = PORT_SEARCH_RADIUS
        
        for land_nid in land_node_ids:
            if land_nid == sea_nid:
                continue
            land_node = nodes_by_id[land_nid]
            dist = haversine_distance(sea_lat, sea_lon, land_node['lat'], land_node['lon'])
            if dist < best_dist:
                best_dist = dist
                best_land = land_nid
        
        if best_land is not None:
            land_node = nodes_by_id[best_land]
            # Add a "port" edge connecting sea to land
            edge_idx = len(edges)
            port_edge = {
                'from': sea_nid,
                'to': best_land,
                'length': round(best_dist, 3),
                'type': 'port',  # Special type for land/sea transitions
                'coords': [
                    [round(sea_lat, 5), round(sea_lon, 5)],
                    [round(land_node['lat'], 5), round(land_node['lon'], 5)]
                ]
            }
            edges.append(port_edge)
            port_edges_added += 1
            
            # Add to spatial index
            for coord in port_edge['coords']:
                lat, lon = coord
                cell = grid_cell(lat, lon)
                if edge_idx not in spatial_index[cell]:
                    spatial_index[cell].append(edge_idx)
    
    print(f"Added {port_edges_added} port connector edges")
    
    # Convert nodes dict to array (sorted by id)
    nodes_array = [None] * len(nodes)
    for key, node in nodes.items():
        nodes_array[node['id']] = {'lat': round(node['lat'], 5), 'lon': round(node['lon'], 5)}
    
    # Build output
    graph = {
        'nodes': nodes_array,
        'edges': edges,
        'spatialIndex': dict(spatial_index),
        'cellSize': 0.25
    }
    
    # Write output
    output_file = 'itinere_graph.json'
    with open(output_file, 'w') as f:
        json.dump(graph, f, separators=(',', ':'))
    
    # Calculate file size
    import os
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"Written to {output_file} ({size_mb:.2f} MB)")
    
    # Also write a summary
    print(f"\nGraph summary:")
    print(f"  Nodes: {len(nodes_array)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Spatial index cells: {len(spatial_index)}")

if __name__ == '__main__':
    main()
