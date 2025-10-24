# Historical Map Visualization Tool

## Overview
An interactive map visualization tool built with Leaflet.js that displays historical locations with labeled markers, optional walking paths between them, estimated ancient travel times, and toggleable country borders. Fully customizable via URL query parameters.

## Project Type
- Static HTML application
- No build process required
- Uses CDN-hosted libraries (Leaflet.js)
- Python HTTP server for local development

## Recent Changes
- 2025-10-24: Initial Replit environment setup and feature implementation
  - Set up Python HTTP server on port 5000
  - Configured deployment settings
  - Customized popup styling to match reference design (white background, large blue titles, gray subtitles)
  - Added permanent blue marker labels showing location names
  - Integrated OSRM API for walking paths between consecutive locations
  - Implemented ancient travel time estimation (60% walking at 25km/day, 40% boat at 100km/day)
  - Made walking paths and travel time optional via URL parameters
  - Added toggleable country borders overlay using Natural Earth GeoJSON data
  - Implemented layer control for base maps and border overlay

## Features
- **Custom Locations**: Specify points via URL parameters
- **Rich Popups**: Click markers to see detailed historical information with custom styling
- **Permanent Labels**: Location names displayed on blue labels above markers
- **Walking Paths**: Optional blue paths showing walking routes between locations (OSRM API)
- **Travel Time**: Optional ancient travel time estimation displayed on map
- **Country Borders**: Toggleable thick border overlay for political boundaries
- **Base Map Options**: Switch between Clean (minimal) and Detailed (with roads) views
- **URL-Driven**: All features controllable via query parameters

## Architecture
- Single HTML file (`map.html`) containing:
  - CSS styling for map, popups, markers, and labels
  - JavaScript for geocoding, routing, and map rendering
  - Leaflet.js integration via CDN
- APIs Used:
  - OpenStreetMap Nominatim API for geocoding locations
  - OSRM (routing.openstreetmap.de) for walking route calculations
  - Natural Earth GeoJSON for country boundary data
- No backend or database required (stateless)

## URL Parameters
- `points` - Pipe-separated locations (e.g., `Rome,Italy|Ephesus,Turkey`)
- `labels` - Pipe-separated labels with `%0A` for newlines
- `path` - Set to `false` to hide walking paths (default: shown)
- `travelTime` - Set to `false` to hide travel time display (default: shown)

## Map Controls
**Layer Control (upper right):**
- Base Layers: Clean (default), Detailed
- Overlays: Country Borders (toggleable, on by default)

## Running the Project
The project runs a simple Python HTTP server to serve the static HTML file on port 5000.
