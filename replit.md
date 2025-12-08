# Historical Map Visualization Tool

## Overview
This project is an interactive map visualization tool built with Leaflet.js, designed to display historical locations with labeled markers, optional walking paths, estimated ancient travel times, and toggleable country and Roman road overlays. It is fully customizable via URL query parameters. The tool aims to provide an accessible and interactive way to explore historical journeys and locations, with a focus on ease of deployment and LLM-friendly documentation.

## User Preferences
- **CRITICAL:** Whenever adding or updating features, ALWAYS update the LLM instructions in `llm.md`.
- `llm.md` is a single Markdown file following web standards for LLM instruction documentation.
- This static file works with GitHub Pages and must always reflect the latest functionality.
- Markdown format is both LLM-friendly and human-readable when rendered on GitHub.

## System Architecture
The tool uses a hybrid architecture with a static frontend and a Flask backend for a screenshot API (primarily for Replit development). The frontend `index.html` file integrates Leaflet.js via CDN and handles all map rendering, geocoding, and routing logic. `llm.md` serves as the comprehensive, web-standard documentation for LLM instructions.

**UI/UX Decisions:**
- **Two Location Types:** Chronological (blue markers, connected by paths) and Reference (red markers, standalone).
- **Responsive Drawer Interface:** Markers open a detailed information drawer, which acts as a bottom sheet on mobile (with swipe gestures and pull handle) and a centered modal on desktop. This unified UX eliminates mobile detection complexity.
- **Permanent Labels:** Location names are displayed directly above markers (blue for chronological, red for reference).
- **Travel Line and Time Overlay:** Displays color-coded travel paths (purple gradient for accessibility), numbered circular badges along paths, and a travel time information box with legend.
- **Route Type Selector:** "Land Only" (routes around water) vs "Use Water" (detects Mediterranean crossings, calculates sailing at 4 knots/7.4 km/h). When Use Water is enabled, shows land vs. sea breakdown with anchor icons for water segments.
- **Transport Mode Selector:** 4 historical land travel speed options: Walking (4 km/h), Ox cart (2 km/h), Pack animal (4.5 km/h), Horse courier (6 km/h). Selector appears when Travel Line overlay is enabled and dynamically recalculates travel times.
- **Toggleable Overlays:** Includes Country Borders and Roman Roads (16,554 road segments from itiner-e dataset).
- **Map Title:** Optional `title` URL parameter displays a centered title above the map.
- **Loading Progress Overlay:** A full-screen indicator with spinner shows real-time status during map initialization, geocoding, and route calculation.

**Technical Implementations:**
- **URL-Driven Customization:** All features are controllable via query parameters, with `chronoLocationsAndLabels` and `referenceLocationsAndLabels` using a `Location~Label|Location~Label` format to eliminate count mismatch errors.
- **Geocoding Best Practices:** `llm.md` includes detailed best practices for geocoding, addressing issues like province/city center discrepancies and ancient city names, including a "Coordinate Override" fallback.
- **Client-side Cache-busting:** For Replit development, a timestamp-based cache-busting mechanism is appended to URLs to ensure fresh previews.
- **Static Deployment:** Designed for easy deployment to GitHub Pages, serving static files directly without a backend.

**File Structure:**
- `index.html`: Main map application (static).
- `llm.md`: LLM instruction documentation (static, web standard).
- `README.md`: GitHub-facing project documentation.
- `server.py`: Flask backend with screenshot API (Replit only).
- `roman_roads.ndjson`: itiner-e Roman road network data (16,554 segments, 39MB).
- `country_borders.geojson`: Natural Earth country boundary data (local).
- `sailing_data.json`: Mendeley ancient Mediterranean sailing routes (83 ports, 361 routes).

## External Dependencies
- **Mapping Library:** Leaflet.js (CDN-hosted)
- **Map Tile Sources:**
    - DARE (Digital Atlas of the Roman Empire) - dh.gu.se
    - CartoDB Positron (modern clean map)
    - OpenStreetMap (modern detailed map)
- **Geocoding API:** OpenStreetMap Nominatim API
- **Routing API:** OSRM (routing.openstreetmap.de) for walking route calculations
- **Country Boundary Data:** Natural Earth GeoJSON (downloaded locally)
- **Roman Roads Data:** itiner-e dataset (downloaded locally as `roman_roads.ndjson`)
- **Sailing Routes Data:** Mendeley ancient Mediterranean shipping network (downloaded locally as `sailing_routes.json`, 58 ports, 257 routes)
- **Screenshot API (Replit only):** Playwright with system Chromium from Nix.