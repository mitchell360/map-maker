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
- **CRITICAL:** Whenever adding or updating features, ALWAYS update the LLM instructions:
  - `llm.md` - Single Markdown file following web standards for LLM instruction documentation
- This static file works with GitHub Pages and must always reflect the latest functionality
- Markdown format is both LLM-friendly and human-readable when rendered on GitHub

## Recent Changes
- 2025-12-08: **ENHANCED README.md** - Added comprehensive GitHub-facing documentation
  - Added project overview, features list, quick example URL
  - Included URL format reference and link to llm.md for LLM instructions
  - Added technology stack and MIT license
  - README is concise (52 lines) and links to llm.md for detailed instructions
- 2025-10-28: **ADDED GEOCODING BEST PRACTICES SECTION** - Critical documentation to prevent location errors
  - Added prominent "Geocoding Best Practices" section in llm.md after Service Overview
  - Created table of common geocoding mistakes (e.g., Philadelphia,Turkey → Alasehir,Turkey)
  - Documented pattern for handling ancient city names with modern geocoding
  - Fixed Example 6 (Seven Churches) to use correct modern city names
  - Updated Step 1 to emphasize using modern names for accurate geocoding
  - Prevents ancient city names from plotting to wrong locations (e.g., Philadelphia, USA instead of Turkey)
- 2025-10-28: **ENHANCED TITLE PARAMETER DOCUMENTATION** - Comprehensive llm.md updates
  - Added detailed `title` parameter documentation with use cases and styling details
  - Added 6 complete working examples demonstrating title parameter usage
  - Updated step-by-step construction process to include optional title parameter
  - Added title encoding examples to encoding reference table
  - Examples include: "Key Locations in Galatians", "The Seven Churches of Revelation", and more
- 2025-10-28: **REMOVED BACKWARD COMPATIBILITY** - Simplified codebase by removing legacy parameter support
  - Removed all backward compatibility code for old `chrono`/`chronoLabels` parameter format
  - Only supports current `chronoLocationsAndLabels` and `referenceLocationsAndLabels` parameters
  - Removed deprecation warnings and old format parsing logic
  - Updated all documentation (llm.md, replit.md) to reference only current format
  - Cleaner, simpler codebase with single clear API contract
- 2025-10-28: **ADDED MAP TITLE AND LOADING PROGRESS OVERLAY**
  - **Map Title:** Optional `title` URL parameter displays centered title above map with elegant serif styling
  - Default title "Paul's Missionary Journeys" shown when no title parameter provided
  - Title has z-index:3100 to appear above loading overlay (visible during entire session)
  - **Loading Progress Overlay:** Full-screen loading indicator with spinner and real-time status
  - Shows "Initializing map...", "Loading locations..." with geocoding progress (e.g., "Geocoding: Antioch,Turkey (1/5)")
  - Displays route calculation progress (e.g., "Route 2 of 3: Philippi → Ephesus")
  - Automatically hides when map is fully rendered
  - **Bug Fixes:** Fixed template literal syntax error in numbered badge HTML, fixed double-decoding issue in title parameter
  - **Documentation:** Updated `llm.md` with complete title parameter documentation
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
- 2025-10-28: **URL PARAMETER ARCHITECTURE** - Redesigned to eliminate count mismatch errors
  - `chronoLocationsAndLabels` and `referenceLocationsAndLabels` parameters combine location and label data
  - Uses `~` (tilde) separator to bind each location to its label: `Location~Label|Location~Label`
  - Eliminates impossible-to-debug mismatch errors when location count ≠ label count
  - Implemented TBD placeholder handling for incomplete data
  - Removed legacy format support for cleaner, more maintainable codebase
  - Updated `llm.md` with complete format documentation
- 2025-10-28: **CONSOLIDATED LLM INSTRUCTIONS TO SINGLE FILE**
  - **Created `llm.md`** - Single source of truth following web standards for LLM instruction documentation
  - Replaced separate `llm-instructions.html` and `llm-instructions.json` files (deleted to prevent drift)
  - Markdown format is both LLM-friendly and beautifully rendered on GitHub Pages
  - Updated "?" button to open `llm.md` in new window (`target="_blank"`)
  - Single file is easier to maintain and impossible to get out of sync
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
- Static instruction file for LLMs:
  - `llm.md` - Comprehensive Markdown guide (follows web standards for LLM instruction documentation)
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

Each parameter combines locations and labels together, eliminating count mismatch errors.

**Chronological Locations (Blue Markers - Connected Journey):**
- `chronoLocationsAndLabels` - Location-label pairs using `~` separator, multiple pairs with `|`
- Format: `Location1~Label1|Location2~Label2|Location3~Label3`
- Example: `chronoLocationsAndLabels=Antioch,Turkey~Antioch%0A47-48 AD|Rome,Italy~Rome%0A62 AD`

**Reference Locations (Red Markers - Standalone):**
- `referenceLocationsAndLabels` - Location-label pairs using `~` separator, multiple pairs with `|`
- Format: `Location1~Label1|Location2~Label2`
- Example: `referenceLocationsAndLabels=Jerusalem,Israel~Jerusalem%0A33 AD%0A%0AThe Church's birthplace`

**Example URL:**
```
?chronoLocationsAndLabels=Antioch,Turkey~Antioch%0A47-48 AD|Rome,Italy~Rome%0A62 AD
&referenceLocationsAndLabels=Jerusalem,Israel~Jerusalem%0A33 AD%0A%0AThe Church's birthplace
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
- URL parameters work directly: `https://mitchell360.com/map-maker/?chronoLocationsAndLabels=Location1~Label1|Location2~Label2`

## File Structure
```
.
├── index.html              # Main map application (static)
├── llm.md                  # LLM instruction documentation (static, web standard)
├── README.md               # GitHub-facing project documentation
└── replit.md              # Project documentation (agent memory)
```

All files are static and work identically in Replit development and GitHub Pages deployment.
