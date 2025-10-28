# Historical Map Visualization Tool

## Overview
An interactive map visualization tool built with Leaflet.js that displays historical locations with labeled markers, optional walking paths between them, estimated ancient travel times, and toggleable country borders. Fully customizable via URL query parameters.

## Project Type
- **Pure static site** - No custom server code
- Static HTML files ready for GitHub Pages deployment
- No build process required
- Uses CDN-hosted libraries (Leaflet.js)
- Simple Python static file server for Replit development/testing

## User Preferences & Development Practices
- **CRITICAL:** Whenever adding or updating features, ALWAYS update the LLM instructions in both:
  - `llm-instructions.html` - Human-readable formatted instructions
  - `llm-instructions.json` - Machine-readable structured data
- These static files work with GitHub Pages and must always reflect the latest functionality
- Keep both HTML and JSON formats synchronized with current URL parameters and features

## Recent Changes
- 2025-10-28: **ADDED MAP TITLE AND LOADING PROGRESS OVERLAY**
  - **Map Title:** Optional `title` URL parameter displays centered title above map with elegant serif styling
  - Default title "Paul's Missionary Journeys" shown when no title parameter provided
  - Title has z-index:3100 to appear above loading overlay (visible during entire session)
  - **Loading Progress Overlay:** Full-screen loading indicator with spinner and real-time status
  - Shows "Initializing map...", "Loading locations..." with geocoding progress (e.g., "Geocoding: Antioch,Turkey (1/5)")
  - Displays route calculation progress (e.g., "Route 2 of 3: Philippi → Ephesus")
  - Automatically hides when map is fully rendered
  - **Bug Fixes:** Fixed template literal syntax error in numbered badge HTML, fixed double-decoding issue in title parameter
  - **Documentation:** Updated both `llm-instructions.html` and `llm-instructions.json` with complete title parameter documentation
- 2025-10-28: **ADDED AUTOMATIC CACHE-BUSTING** - For Replit development preview only
  - Automatically appends `?_cb=[timestamp]` to URL if not present
  - Bypasses Replit's aggressive preview iframe caching
  - Ensures updates always appear without manual cache clearing
  - **NOTE:** This is ONLY needed for Replit development - GitHub Pages doesn't have this caching issue
  - Pure client-side JavaScript solution (no server code)
- 2025-10-28: **MAJOR SIMPLIFICATION** - Unified drawer UX for all devices, eliminated mobile detection complexity
  - **Removed isMobile() function** - No more runtime mobile detection logic
  - **Single interaction model** - All markers use drawer click handler (no if/else branching)
  - **CSS-driven responsive design** - Media queries handle all viewport adaptations automatically
  - **Desktop:** Centered modal with scale animation, larger fonts, no pull handle
  - **Mobile:** Bottom sheet with swipe gestures, pull handle visible
  - **Fixed pointer-events bug** - Hidden drawer no longer blocks map interactions
  - Added visibility:hidden + pointer-events:none to closed drawer for proper map usability
  - Cleaner, more maintainable codebase with single code path for all devices
  - **Instructions button** - Now always displays as blue circular "?" button on all devices
- 2025-10-28: **BREAKING CHANGE** - Redesigned URL parameter architecture to eliminate count mismatch errors
  - **NEW FORMAT:** `chronoLocationsAndLabels` and `referenceLocationsAndLabels` parameters combine location and label data
  - Uses `~` (tilde) separator to bind each location to its label: `Location~Label|Location~Label`
  - Eliminates impossible-to-debug mismatch errors when location count ≠ label count
  - Backward compatible: old `chrono/chronoLabels` format still works with console warning
  - Implemented TBD placeholder handling for incomplete data
  - Updated both `llm-instructions.html` and `llm-instructions.json` with new format
- 2025-10-26: Added static LLM instructions files
  - **Created `llm-instructions.html`** - beautifully formatted HTML page with comprehensive URL construction instructions for LLMs
  - **Created `llm-instructions.json`** - structured JSON version for programmatic access
  - Both files are static and work with GitHub Pages hosting
  - Instructions include parameter definitions, examples, encoding rules, construction steps, and tips
  - Server prints availability on startup for local development
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
  - Chronological locations (blue markers) - Connected by color-coded travel paths in order
  - Reference locations (red markers) - Standalone historical context points
- **Custom Locations**: Specify both types via URL parameters
- **Responsive Drawer Interface**: Click markers to see detailed historical information in a drawer (bottom sheet on mobile, centered modal on desktop)
- **Permanent Labels**: Location names displayed above markers (blue for chronological, red for reference)
- **Travel Line and Time**: Optional overlay showing:
  - Color-coded travel paths between chronological locations (purple gradient for accessibility)
  - White stroke border around lines for high contrast against map backgrounds
  - Numbered circular badges along each path (all segment 1 arrows show "1", segment 2 show "2", etc.)
  - White circles with colored borders matching the segment color
  - Travel time information box with color legend matching line colors
  - Estimated ancient travel time for each segment and total journey
  - Uses OSRM API for walking route calculations
- **Multiple Base Maps**:
  - Ancient World (DARE) - Default, Digital Atlas of the Roman Empire
  - Modern Clean - Minimal contemporary map
  - Modern Detailed - Full modern map with roads
- **Toggleable Overlays**:
  - Country Borders - Political boundaries
  - Travel Line and Time - Color-coded routes with travel duration display
- **URL-Driven**: All features controllable via query parameters

## Architecture
- Single HTML file (`index.html`) containing:
  - CSS styling for map, popups, markers, and labels
  - JavaScript for geocoding, routing, and map rendering
  - Leaflet.js integration via CDN
- Static instruction files for LLMs:
  - `llm-instructions.html` - Human-readable formatted guide
  - `llm-instructions.json` - Machine-readable structured data
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

### NEW FORMAT (Recommended - 2025-10-28)
Each parameter combines locations and labels together, eliminating count mismatch errors.

**Chronological Locations (Blue Markers - Connected Journey):**
- `chronoLocationsAndLabels` - Location-label pairs using `~` separator, multiple pairs with `|`
- Format: `Location1~Label1|Location2~Label2|Location3~Label3`
- Example: `chronoLocationsAndLabels=Antioch,Turkey~Antioch%0A47-48 AD|Rome,Italy~Rome%0A62 AD`

**Reference Locations (Red Markers - Standalone):**
- `referenceLocationsAndLabels` - Location-label pairs using `~` separator, multiple pairs with `|`
- Format: `Location1~Label1|Location2~Label2`
- Example: `referenceLocationsAndLabels=Jerusalem,Israel~Jerusalem%0A33 AD%0A%0AThe Church's birthplace`

**Example URL (New Format):**
```
?chronoLocationsAndLabels=Antioch,Turkey~Antioch%0A47-48 AD|Rome,Italy~Rome%0A62 AD
&referenceLocationsAndLabels=Jerusalem,Israel~Jerusalem%0A33 AD%0A%0AThe Church's birthplace
```

### OLD FORMAT (Deprecated - Still Supported)
Legacy parameters with separate location and label arrays. Still works but displays console warning.

- `chrono` - Pipe-separated locations
- `chronoLabels` - Pipe-separated labels (must match location count)
- `reference` - Pipe-separated locations
- `referenceLabels` - Pipe-separated labels (must match location count)

**Migration:** Use new combined format to avoid count mismatch errors.

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
- Overlays: Country Borders, Travel Line and Time (all hidden by default)

**Travel Line and Time Display:**
When enabled, shows color-coded travel paths where each segment between consecutive locations uses a different shade of purple (for web accessibility). Each line includes:
- White stroke border for high contrast against the ancient map background
- Numbered circular badges at regular intervals (e.g., all arrows on first segment show "1", second segment show "2")
- White circles with black numbers and colored borders matching each segment
- Color legend in the travel time information box matching the purple gradient
- Estimated travel duration for each leg and the total journey

## Running the Project
**For Replit Development/Testing:**
- Uses Python's built-in static file server: `python3 -m http.server 5000`
- Serves files at http://localhost:5000/
- No custom server logic - pure static file serving

**For GitHub Pages Deployment:**
- Files are served as-is from the repository
- `index.html` is automatically served at the root path
- URL parameters work directly: `https://mitchell360.com/map-maker/?chrono=Location1|Location2`

## File Structure
```
.
├── index.html              # Main map application (static)
├── llm-instructions.html   # Human-readable LLM instructions (static)
├── llm-instructions.json   # Machine-readable LLM instructions (static)
└── replit.md              # Project documentation
```

All files are static and work identically in Replit development and GitHub Pages deployment.
