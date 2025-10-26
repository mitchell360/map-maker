# Historical Map Visualization Tool

## Overview
An interactive map visualization tool built with Leaflet.js that displays historical locations with labeled markers, optional walking paths between them, estimated ancient travel times, and toggleable country borders. Fully customizable via URL query parameters.

## Project Type
- Static HTML application
- No build process required
- Uses CDN-hosted libraries (Leaflet.js)
- Python HTTP server for local development

## Recent Changes
- 2025-10-26: Simplified to use default Leaflet tooltip behavior
  - **Removed custom leader line positioning code** - simplified to use Leaflet's built-in tooltip system
  - **Clean, minimal labels** positioned directly above markers using default `bindTooltip()`
  - Blue tooltips for chronological locations, red tooltips for reference locations
  - Much cleaner and more maintainable code
- 2025-10-24: Core functionality implementation
  - **Updated to Leaflet 1.9.4** (latest stable version) with integrity hashes for security
  - **Removed buggy third-party libraries** - uses only stable Leaflet core features
  - Created two-group location system: chronological (blue markers, connected) and reference (red markers, standalone)
  - Integrated DARE (Digital Atlas of the Roman Empire) as default ancient world map
  - Implemented ancient travel time estimation (60% walking at 25km/day, 40% boat at 100km/day)
  - Added toggleable overlays: walking paths, travel time display, country borders

## Features
- **Two Location Types**:
  - Chronological locations (blue markers) - Connected by walking paths in order
  - Reference locations (red markers) - Standalone historical context points
- **Custom Locations**: Specify both types via URL parameters
- **Rich Popups**: Click markers to see detailed historical information with custom styling
- **Permanent Labels**: Location names displayed above markers (blue for chronological, red for reference)
- **Walking Paths**: Optional blue paths showing walking routes between chronological locations (OSRM API)
- **Travel Time**: Optional ancient travel time estimation for chronological journey
- **Multiple Base Maps**:
  - Ancient World (DARE) - Default, Digital Atlas of the Roman Empire
  - Modern Clean - Minimal contemporary map
  - Modern Detailed - Full modern map with roads
- **Toggleable Overlays**:
  - Country Borders - Political boundaries
  - Walking Paths - Route visualization
  - Travel Time - Journey duration display
- **URL-Driven**: All features controllable via query parameters

## Architecture
- Single HTML file (`map.html`) containing:
  - CSS styling for map, popups, markers, and labels
  - JavaScript for geocoding, routing, and map rendering
  - Leaflet.js integration via CDN
- Map Tile Sources:
  - DARE (Digital Atlas of the Roman Empire) - dh.gu.se
  - CartoDB Positron (modern clean)
  - OpenStreetMap (modern detailed)
- APIs Used:
  - OpenStreetMap Nominatim API for geocoding locations
  - OSRM (routing.openstreetmap.de) for walking route calculations
  - Natural Earth GeoJSON for country boundary data
- No backend or database required (stateless)

## URL Parameters

### Chronological Locations (Blue Markers)
- `chrono` - Pipe-separated locations (e.g., `Antioch,Turkey|Philippi,Greece|Rome,Italy`)
- `chronoLabels` - Pipe-separated labels with `%0A` for newlines

### Reference Locations (Red Markers)
- `reference` - Pipe-separated locations (e.g., `Jerusalem,Israel|Athens,Greece`)
- `referenceLabels` - Pipe-separated labels with `%0A` for newlines

### Example URL
```
?chrono=Antioch,Turkey|Rome,Italy
&chronoLabels=Antioch%0A47-48 AD|Rome%0A62 AD
&reference=Jerusalem,Israel
&referenceLabels=Jerusalem%0AThe Church's birthplace
```

## Default Test Data
**Chronological Journey (Blue):**
- Antioch, Turkey (47-48 AD)
- Philippi, Greece (49-50 AD)
- Ephesus, Turkey (52-54 AD)
- Rome, Italy (62 AD)

**Reference Location (Red):**
- Jerusalem, Israel (33 AD) - Church's birthplace and site of Pentecost

## Map Controls
**Layer Control (upper right):**
- Base Layers: Ancient World (default), Modern Clean, Modern Detailed
- Overlays: Country Borders, Walking Paths, Travel Time (all hidden by default)

## Running the Project
The project runs a simple Python HTTP server to serve the static HTML file on port 5000.
