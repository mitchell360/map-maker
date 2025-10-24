# Map Maker

## Overview
A simple static web application that displays interactive maps using Leaflet.js. Users can specify locations via URL query parameters to create custom maps with markers and labels.

## Project Type
- Static HTML application
- No build process required
- Uses CDN-hosted libraries (Leaflet.js)

## Recent Changes
- 2025-10-24: Initial Replit environment setup
  - Added Python HTTP server for serving static files
  - Configured workflow to run on port 5000
  - Set up deployment configuration

## Architecture
- Single HTML file (`map.html`) containing:
  - CSS styling for map and popups
  - JavaScript for geocoding and map rendering
  - Leaflet.js integration via CDN
- Uses OpenStreetMap Nominatim API for geocoding
- No backend or database required

## Running the Project
The project runs a simple Python HTTP server to serve the static HTML file on port 5000.
