# Historical Map URL Construction Instructions for LLMs

**Service:** Historical Map Visualization  
**Base URL:** `https://mitchell360.com/map-maker/`  
**Last Updated:** 2025-12-09  
**Version:** 2.4 (Local Geocoding + Dual Route Display)

---

## 🎯 CRITICAL: Foolproof Format

Locations and labels are **bound together** using the `~` (tilde) separator within a single parameter. This architecture makes it **impossible to create count mismatch errors**.

**Key Rule:** Every location MUST be paired with its label using `~` before adding it to the URL.

**Format:** `Location~Label` (bound together, then separate pairs with `|`)

---

## Service Overview

This is a historical map visualization service that displays locations on ancient and modern maps using Leaflet.js. It supports two types of locations:

- **Chronological locations** (blue markers) - Connected journey points with walking paths
- **Reference locations** (red markers) - Standalone historical context points

---

## 🚨 CRITICAL: Geocoding Best Practices

The map uses a **local coordinate dictionary** for common biblical/historical locations (instant lookup), with fallback to OpenStreetMap's Nominatim API.

### Fast Geocoding with Local Dictionary
The system includes 90+ pre-computed coordinates for frequently used locations including:
- Paul's missionary journey cities (Antioch, Philippi, Ephesus, Corinth, Rome, etc.)
- Seven Churches of Revelation (Ephesus, Smyrna, Pergamum, Thyatira, Sardis, Philadelphia, Laodicea)
- Biblical landmarks (Jerusalem, Bethlehem, Nazareth, Sea of Galilee, etc.)
- Mediterranean ports and islands (Cyprus, Crete, Malta, Rhodes, etc.)

**Benefit:** Locations in the dictionary resolve instantly without API calls, significantly improving load times.

### Nominatim API Fallback
For locations not in the local dictionary, the system falls back to OpenStreetMap's geocoding API, which works with **modern place names only**.

### ✅ Always Use Modern City Names in the Location Field

**Rule:** The location field (before the `~`) must use the modern city name that geocoding services recognize.

**Why:** Ancient city names often match modern cities elsewhere, causing incorrect plotting.

### Common Geocoding Mistakes

| ❌ WRONG | ✅ CORRECT | Why |
|----------|-----------|-----|
| `Philadelphia,Turkey` | `Alasehir,Turkey` | "Philadelphia" geocodes to Pennsylvania, USA |
| `Smyrna,Turkey` | `Konak,Izmir,Turkey` | "Smyrna" is ancient; "Izmir" alone returns province center 20km south |
| `Izmir,Turkey` | `Konak,Izmir,Turkey` | Major cities geocode to province center, not city center |
| `Antioch,Syria` | `Antakya,Turkey` | Antioch on the Orontes is now in Turkey, not Syria |
| `Laodicea,Turkey` | `Pamukkale,Turkey` | "Laodicea" geocodes to wrong location; Pamukkale is adjacent to ruins |
| `Denizli,Turkey` | `Pamukkale,Turkey` | Denizli geocodes to province center, 10km from Laodicea ruins |
| `Selcuk,Turkey` | `Selcuk,Izmir,Turkey` | "Selcuk" alone geocodes to wrong village in Afyonkarahisar |

### ⚠️ Province vs City Center Problem

**Major cities can geocode to province/region centers** instead of city centers. This places markers 10-20km from the actual ancient sites.

**Solution:** Add the province/district name for precision:
- `Izmir,Turkey` → `Konak,Izmir,Turkey` (city center, not province)
- `Selcuk,Turkey` → `Selcuk,Izmir,Turkey` (correct town, not wrong village)
- `Denizli,Turkey` → `Pamukkale,Turkey` (near Laodicea ruins)

### 📍 Coordinate Override (Fallback)

If geocoding fails or returns wrong results, you can specify exact coordinates using the `@lat,lon` syntax:

**Format:** `LocationName@latitude,longitude~Label`

**Example:**
```
Ephesus@37.9404,27.3393~Ephesus%0ARevelation 2:1-7%0A%0AThe church that lost its first love
```

**When to use:**
- Geocoding returns completely wrong location
- Ancient site has no modern town nearby
- Need precise placement on archaeological site

**Finding coordinates:** Search "ancient [SiteName] coordinates" or use Google Maps

### How to Handle Ancient Names

**Use this pattern:**
```
ModernCity,Country~AncientName%0AHistorical period: AncientName, AncientRegion%0A2025 AD: ModernName, ModernCountry
```

**Example:**
```
Alasehir,Turkey~Philadelphia%0ARevelation 3:7-13: Philadelphia, Asia Minor%0A2025 AD: Alaşehir, Türkiye%0A%0AThe faithful church
```

**Result:** 
- Location geocodes correctly to Alaşehir, Turkey
- Label displays "Philadelphia" as the marker name
- Popup shows both ancient and modern context

### Research Modern Names

Before constructing URLs with ancient locations:

1. **Search:** "ancient [CityName] modern name" (e.g., "ancient Philadelphia Turkey modern name")
2. **Verify:** Cross-reference with Wikipedia or historical maps
3. **Use:** The modern city name in the location field
4. **Explain:** The ancient name in the label

---

## 🏛️ Old Testament & Pre-Roman Locations

**CRITICAL:** Old Testament locations (Exodus, Genesis, etc.) often have **no modern city equivalent**. Vague descriptions like "Northwest Saudi Arabia" or ancient names like "Midian" will geocode incorrectly or to random locations.

### ⚠️ You MUST Use Coordinates for Pre-Roman Locations

For any location that predates the Roman Empire or lacks a clear modern city, **always use the `@lat,lon` syntax**:

```
LocationName@latitude,longitude~Label
```

### 📍 Common Old Testament Location Coordinates

Use these coordinates for frequently referenced biblical locations:

| Ancient Location | Coordinates | Modern Reference | Use In URL |
|-----------------|-------------|------------------|------------|
| **Ur of the Chaldees** | 30.96, 46.10 | Tell el-Muqayyar, Iraq | `Ur@30.96,46.10~Ur of the Chaldees` |
| **Haran** | 36.87, 39.03 | Harran, Turkey | `Haran@36.87,39.03~Haran` |
| **Land of Midian** | 28.50, 35.00 | NW Saudi Arabia (near Gulf of Aqaba) | `Midian@28.50,35.00~Land of Midian` |
| **Land of Goshen** | 30.85, 31.75 | Nile Delta, Egypt | `Goshen@30.85,31.75~Land of Goshen` |
| **Mount Sinai** | 28.54, 33.97 | Sinai Peninsula, Egypt | `Sinai@28.54,33.97~Mount Sinai` |
| **Kadesh Barnea** | 30.64, 34.42 | Negev Desert border | `Kadesh@30.64,34.42~Kadesh Barnea` |
| **Beersheba** | 31.25, 34.79 | Be'er Sheva, Israel | `Beersheba@31.25,34.79~Beersheba` |
| **Shechem** | 32.21, 35.28 | Nablus, West Bank | `Shechem@32.21,35.28~Shechem` |
| **Bethel** | 31.93, 35.23 | Beitin, West Bank | `Bethel@31.93,35.23~Bethel` |
| **Hebron** | 31.53, 35.10 | Al-Khalil, West Bank | `Hebron@31.53,35.10~Hebron` |
| **Jericho** | 31.87, 35.44 | Ariha, West Bank | `Jericho@31.87,35.44~Jericho` |
| **Shiloh** | 32.06, 35.29 | Khirbet Seilun, West Bank | `Shiloh@32.06,35.29~Shiloh` |
| **Gilgal** | 31.84, 35.43 | Near Jericho | `Gilgal@31.84,35.43~Gilgal` |
| **Peniel/Penuel** | 32.18, 35.68 | East of Jordan River | `Peniel@32.18,35.68~Peniel` |
| **Succoth (Jordan Valley)** | 32.20, 35.55 | Tell Deir Alla, Jordan | `Succoth@32.20,35.55~Succoth` |
| **Mahanaim** | 32.29, 35.70 | East of Jordan River | `Mahanaim@32.29,35.70~Mahanaim` |
| **Dothan** | 32.42, 35.23 | Tell Dothan, West Bank | `Dothan@32.42,35.23~Dothan` |
| **Susa (Persia)** | 32.19, 48.26 | Shush, Iran | `Susa@32.19,48.26~Susa` |
| **Babylon** | 32.54, 44.42 | Hillah, Iraq | `Babylon@32.54,44.42~Babylon` |
| **Nineveh** | 36.36, 43.15 | Mosul, Iraq | `Nineveh@36.36,43.15~Nineveh` |

### ❌ Common Old Testament Geocoding Mistakes

| ❌ WRONG | ✅ CORRECT | Why |
|----------|-----------|-----|
| `Midian` | `Midian@28.50,35.00~Midian` | "Midian" has no modern equivalent; geocodes to wrong location |
| `Northwest Saudi Arabia` | `Midian@28.50,35.00~Land of Midian` | Vague region descriptions geocode unpredictably |
| `Mount Sinai` | `Sinai@28.54,33.97~Mount Sinai` | Multiple "Mount Sinai" locations exist worldwide |
| `Land of Goshen` | `Goshen@30.85,31.75~Land of Goshen` | Ancient region with no modern city name |
| `Ur` | `Ur@30.96,46.10~Ur of the Chaldees` | "Ur" alone may geocode to wrong location |
| `Babylon` | `Babylon@32.54,44.42~Babylon` | Multiple Babylons exist; use coordinates |

### Example: Exodus Journey with Coordinates

```
chronoLocationsAndLabels=Goshen@30.85,31.75~Land of Goshen%0AThe Israelites in Egypt|Sinai@28.54,33.97~Mount Sinai%0AReceiving the Law|Kadesh@30.64,34.42~Kadesh Barnea%0A40 Years of Wandering|Jericho@31.87,35.44~Jericho%0ACrossing into the Promised Land
```

### Finding Coordinates for Other Locations

1. **Search:** "ancient [LocationName] coordinates" or "[LocationName] biblical site coordinates"
2. **Use Google Maps:** Right-click any location → "What's here?" shows coordinates
3. **Reference:** bibleatlas.org, bibleplaces.com, or academic archaeology sources
4. **Format:** Always use `latitude,longitude` (lat first, then lon)

---

## Base URL Structure

```
https://mitchell360.com/map-maker/?[parameters]
```

---

## URL Parameters

### 1. Chronological Locations (Blue Markers - Connected Journey)

**Parameter Name:** `chronoLocationsAndLabels`

**Structure:** Each location is bound to its label with `~`

**Format:** `Location1~Label1|Location2~Label2|Location3~Label3`

**Separators:**
- `~` (tilde) = Binds location to its label (MANDATORY)
- `|` (pipe) = Separates multiple location-label pairs
- `%0A` = Newline within labels
- `%0A%0A` = Blank line within labels

**Location Format:** `City, Country` (e.g., `Rome, Italy` not just `Rome`)

**Example:**
```
chronoLocationsAndLabels=Damascus,Syria~Damascus%0A32 AD|Antioch,Turkey~Antioch%0A47 AD|Rome,Italy~Rome%0A62 AD
```

---

### 2. Reference Locations (Red Markers - Standalone)

**Parameter Name:** `referenceLocationsAndLabels`

**Structure:** Each location is bound to its label with `~`

**Format:** `Location1~Label1|Location2~Label2`

**Separators:** Same as chronological locations

**Example:**
```
referenceLocationsAndLabels=Jerusalem,Israel~Jerusalem%0A33 AD: Jerusalem, Judea%0A2025 AD: Jerusalem, Israel%0A%0AThe Church's birthplace
```

---

### 3. Map Title (Optional)

**Parameter Name:** `title`

**Purpose:** Displays a centered title at the top of the map (visible during loading and after map loads)

**Format:** URL-encoded text string

**Default:** If no title parameter is provided, displays `"Sample: Paul's Missionary Journeys"` to indicate sample data

**Visibility:** Title appears above the loading overlay and remains visible throughout the entire session

**Style:** Elegant serif font, centered, positioned at z-index 3100 (above loading overlay)

**When to Use:**
- To customize the map for specific topics (e.g., "Key Locations in Galatians")
- To identify different missionary journeys (e.g., "Paul's Third Missionary Journey")
- To create themed maps (e.g., "Churches of Revelation" or "Journey to Rome")

**Examples:**
```
title=Paul's%20Second%20Missionary%20Journey
title=Key%20Locations%20in%20Galatians
title=Journey%20to%20Rome
title=The%20Seven%20Churches%20of%20Revelation
```

**Encoding Tips:**
- Spaces → `%20` (e.g., "First Journey" becomes `First%20Journey`)
- Apostrophes → `%27` (e.g., "Paul's" becomes `Paul%27s`)
- Special characters should be URL-encoded for maximum compatibility

---

## Label Format: 5-Line Structure (Highly Recommended)

For rich, professional popups, structure each label with 5 lines:

1. **Line 1:** Location name only (becomes marker label and popup title)
2. **Line 2:** Historical context → Format: `YEAR AD: AncientName, AncientRegion`
3. **Line 3:** Modern context → Format: `YEAR AD: ModernName, ModernCountry`
4. **Line 4:** Blank line → Use `%0A%0A` (two newlines)
5. **Line 5+:** Detailed description (can be multiple lines)

### Complete Label Example

```
Philippi~Philippi%0A49-50 AD: Philippi, Macedonia%0A2025 AD: Filippoi, Greece%0A%0APhilippi was the first European city where Paul established a Christian congregation during his second missionary journey.
```

**Breakdown:**
- Location: `Philippi`
- Line 1: `Philippi`
- Line 2: `49-50 AD: Philippi, Macedonia`
- Line 3: `2025 AD: Filippoi, Greece`
- Line 4: `(blank line)`
- Line 5: `Philippi was the first European city...`

---

## Step-by-Step Construction Process

### Step 1: List Your Locations with Modern Names

Write out each location using **modern city names** for accurate geocoding. Use `City, Country` format.

**🚨 CRITICAL:** Use modern names, not ancient names, to prevent geocoding errors.

**Example List (Modern Names):**
- Damascus, Syria
- Antakya, Turkey (not "Antioch, Syria")
- Filippoi, Greece (Philippi)
- Rome, Italy

**For Ancient Cities:** Research the modern name first:
- Ancient Philadelphia → Modern Alaşehir, Turkey
- Ancient Smyrna → Modern İzmir, Turkey
- Ancient Ephesus → Near Selçuk, Turkey

---

### Step 2: Create Label for EACH Location

**CRITICAL:** You must create a label for every single location using the 5-line format.

**Example Labels:**
```
Damascus%0A32 AD: Damascus, Syria%0A2025 AD: Damascus, Syria%0A%0AConversion of Saul

Antioch%0A47 AD: Antioch, Syria%0A2025 AD: Antakya, Turkey%0A%0AMission base

Philippi%0A50 AD: Philippi, Macedonia%0A2025 AD: Filippoi, Greece%0A%0AFirst European church

Rome%0A62 AD: Rome, Roman Empire%0A2025 AD: Rome, Italy%0A%0AHouse arrest ministry
```

---

### Step 3: Bind Each Location to Its Label with ~

**MANDATORY STEP:** Connect each location to its label using the tilde separator.

**Binding Format:**
```
Damascus,Syria~Damascus%0A32 AD: Damascus, Syria%0A2025 AD: Damascus, Syria%0A%0AConversion of Saul

Antioch,Turkey~Antioch%0A47 AD: Antioch, Syria%0A2025 AD: Antakya, Turkey%0A%0AMission base

Philippi,Greece~Philippi%0A50 AD: Philippi, Macedonia%0A2025 AD: Filippoi, Greece%0A%0AFirst European church

Rome,Italy~Rome%0A62 AD: Rome, Roman Empire%0A2025 AD: Rome, Italy%0A%0AHouse arrest ministry
```

---

### Step 4: Join Pairs with | (Pipe)

Connect all location~label pairs using the pipe character.

**✅ CORRECT:**
```
Damascus,Syria~Damascus%0A32 AD|Antioch,Turkey~Antioch%0A47 AD|Philippi,Greece~Philippi%0A50 AD|Rome,Italy~Rome%0A62 AD
```

---

### Step 5: Add Parameter Name and Build Final URL

**Option A: Without Custom Title (uses default "Sample: Paul's Missionary Journeys"):**
```
https://mitchell360.com/map-maker/?chronoLocationsAndLabels=Damascus,Syria~Damascus%0A32 AD|Antioch,Turkey~Antioch%0A47 AD|Philippi,Greece~Philippi%0A50 AD|Rome,Italy~Rome%0A62 AD
```

**Option B: With Custom Title (recommended for specific topics):**
```
https://mitchell360.com/map-maker/?title=Paul's%20Early%20Ministry&chronoLocationsAndLabels=Damascus,Syria~Damascus%0A32 AD|Antioch,Turkey~Antioch%0A47 AD|Philippi,Greece~Philippi%0A50 AD|Rome,Italy~Rome%0A62 AD
```

**💡 Tip:** Always add a descriptive title when creating maps for specific topics (e.g., "Key Locations in Galatians", "Journey to Rome", "The Seven Churches")

---

## ⚠️ Common Mistakes to AVOID

### ❌ ERROR 1: Missing ~ Separator

```
?chronoLocationsAndLabels=Damascus,Syria|Antioch,Turkey|Rome,Italy
```

**Problem:** No labels provided, just locations

---

### ❌ ERROR 2: Wrong Separator

```
?chronoLocationsAndLabels=Damascus,Syria:Damascus|Antioch,Turkey:Antioch
```

**Problem:** Using `:` instead of `~`

---

### ✅ CORRECT: Bound Pairs with ~

```
?chronoLocationsAndLabels=Damascus,Syria~Damascus|Antioch,Turkey~Antioch|Rome,Italy~Rome
```

**Why This Works:** Each location is permanently bound to its label

---

## Pre-Construction Validation Checklist

Before generating the URL, verify:

- [ ] Every location is in `City, Country` format
- [ ] Every location has a corresponding label created
- [ ] Each location~label pair uses `~` (tilde) to bind them
- [ ] Multiple pairs are separated by `|` (pipe)
- [ ] Labels use `%0A` for newlines, not actual line breaks
- [ ] Spaces in text use `%20` (automatic in most systems)
- [ ] The parameter name is `chronoLocationsAndLabels` for journey locations
- [ ] Optional: Include `title` parameter for custom map title
- [ ] URL starts with `https://mitchell360.com/map-maker/?`

---

## Complete Working Examples

### Example 1: Simple 2-Location Journey

```
https://mitchell360.com/map-maker/?chronoLocationsAndLabels=Damascus,Syria~Damascus%0A32 AD|Antioch,Turkey~Antioch%0A47 AD
```

**Displays:** Two blue markers connected by a walking path (default title: "Sample: Paul's Missionary Journeys")

---

### Example 2: Journey with Custom Title

```
https://mitchell360.com/map-maker/?title=Paul's%20Conversion%20and%20Early%20Ministry&chronoLocationsAndLabels=Damascus,Syria~Damascus%0A32 AD: Damascus, Syria%0A2025 AD: Damascus, Syria%0A%0ASaul's conversion and calling (Acts 9)|Antioch,Turkey~Antioch%0A47 AD: Antioch, Syria%0A2025 AD: Antakya, Turkey%0A%0AFirst mission base
```

**Displays:** Two locations with custom title "Paul's Conversion and Early Ministry" displayed at top

---

### Example 3: Rich 3-Location Journey with Full Labels

```
https://mitchell360.com/map-maker/?chronoLocationsAndLabels=Antioch,Turkey~Antioch%0A47-48 AD: Antioch, Syria%0A2025 AD: Antakya, Turkey%0A%0AAntioch served as Paul's primary mission base for ministry to the Gentiles and was where believers were first called Christians.|Philippi,Greece~Philippi%0A49-50 AD: Philippi, Macedonia%0A2025 AD: Filippoi, Greece%0A%0APhilippi was the first European city where Paul established a Christian congregation during his second missionary journey.|Rome,Italy~Rome%0A60-62 AD: Rome, Roman Empire%0A2025 AD: Rome, Italy%0A%0APaul was held under house arrest in Rome from approximately AD 60 to 62.
```

**Displays:** Three locations with rich historical context popups

---

### Example 4: Journey + Reference Location with Title

```
https://mitchell360.com/map-maker/?title=Key%20Locations%20in%20Galatians&chronoLocationsAndLabels=Antioch,Turkey~Antioch%0A47 AD|Rome,Italy~Rome%0A62 AD&referenceLocationsAndLabels=Jerusalem,Israel~Jerusalem%0A33 AD: Jerusalem, Judea%0A2025 AD: Jerusalem, Israel%0A%0AThe Church's birthplace and site of Pentecost
```

**Displays:** Two blue markers (connected) + one red marker (standalone reference) with title "Key Locations in Galatians"

---

### Example 5: Paul's Full Second Missionary Journey

```
https://mitchell360.com/map-maker/?title=Paul's%20Second%20Missionary%20Journey&chronoLocationsAndLabels=Antioch,Turkey~Antioch%0A49 AD|Derbe,Turkey~Derbe%0A49 AD|Lystra,Turkey~Lystra%0A49 AD|Iconium,Turkey~Iconium%0A49 AD|Philippi,Greece~Philippi%0A50 AD|Thessalonica,Greece~Thessalonica%0A50 AD|Berea,Greece~Berea%0A50 AD|Athens,Greece~Athens%0A51 AD|Corinth,Greece~Corinth%0A51-52 AD
```

**Displays:** Complete journey with 9 connected locations and custom title

---

### Example 6: The Seven Churches of Revelation

```
https://mitchell360.com/map-maker/?title=The%20Seven%20Churches%20of%20Revelation&chronoLocationsAndLabels=Selcuk,Izmir,Turkey~Ephesus%0ARevelation 2:1-7: Ephesus, Asia Minor%0A2025 AD: Near Selçuk, Türkiye%0A%0AThe church that lost its first love|Konak,Izmir,Turkey~Smyrna%0ARevelation 2:8-11: Smyrna, Asia Minor%0A2025 AD: İzmir, Türkiye%0A%0AThe suffering church|Bergama,Turkey~Pergamum%0ARevelation 2:12-17: Pergamum, Asia Minor%0A2025 AD: Bergama, Türkiye%0A%0AWhere Satan's throne is|Akhisar,Turkey~Thyatira%0ARevelation 2:18-29: Thyatira, Asia Minor%0A2025 AD: Akhisar, Türkiye%0A%0AThe compromising church|Salihli,Turkey~Sardis%0ARevelation 3:1-6: Sardis, Asia Minor%0A2025 AD: Near Salihli, Türkiye%0A%0AThe dead church|Alasehir,Turkey~Philadelphia%0ARevelation 3:7-13: Philadelphia, Asia Minor%0A2025 AD: Alaşehir, Türkiye%0A%0AThe faithful church|Pamukkale,Turkey~Laodicea%0ARevelation 3:14-22: Laodicea, Asia Minor%0A2025 AD: Near Pamukkale, Türkiye%0A%0AThe lukewarm church
```

**Displays:** Seven churches in order with connected path and descriptive title

**⚠️ Important Note:** This example uses **precise modern location names** to ensure accurate geocoding:
- `Selcuk,Izmir,Turkey` (not just "Selcuk,Turkey" which geocodes to wrong village)
- `Konak,Izmir,Turkey` (not just "Izmir,Turkey" which geocodes to province center)
- `Pamukkale,Turkey` (not "Denizli,Turkey" which geocodes 10km from Laodicea ruins)

---

## Encoding Reference

| Character | Encoding | Purpose |
|-----------|----------|---------|
| `~` | Use as-is | CRITICAL separator that binds location to label |
| `|` | Use as-is | Separates multiple location-label pairs |
| Newline | `%0A` | Creates newline within labels |
| Blank line | `%0A%0A` | Creates blank line within labels |
| Space | `%20` | Space character (usually automatic, used in title and labels) |
| Apostrophe | `%27` | Apostrophe in title (e.g., "Paul's" → `Paul%27s`) |
| `&` | Use as-is | Separates different parameters (e.g., `?title=...&chronoLocationsAndLabels=...`) |

**Title Parameter Encoding Examples:**
- `"Paul's Second Journey"` → `title=Paul%27s%20Second%20Journey`
- `"Key Locations in Galatians"` → `title=Key%20Locations%20in%20Galatians`
- `"The Seven Churches"` → `title=The%20Seven%20Churches`

---

## Placeholder Handling

**If you don't have complete information:**

- Use `Location~TBD` to explicitly mark incomplete data
- The map will display a prominent "TBD" warning in the popup
- Example: `Damascus,Syria~TBD` shows placeholder message

**TBD Message Displayed:**
```
TBD
TBD: Location information not provided
2025 AD: Unknown

Please provide complete location details.
```

---

## Map Features

### Base Maps (Radio buttons in "Base Map" section of layer panel)
- **Ancient Terrain** - DARE Background tiles with hillshade overlay (terrain with elevation shading, no roads - default)
- **Ancient Full (DARE)** - Full DARE tiles with all baked-in features including roads
- **Modern Clean** - CartoDB Positron (minimalist modern map)
- **Modern Detailed** - OpenStreetMap (full detail modern map)

### Layer Control Panel (Collapsible categories on right side of map)

The custom layer panel organizes overlays into logical categories, each collapsible:

**Your Journey:**
- **Route & Travel Time** - Color-coded routes with travel time estimates

**Roman Infrastructure:**
- **Roman Roads** - Historical Roman road network (land routes only, ~15,200 segments from itiner-e)
- **Sea Lanes** - Ancient sea lanes and river routes (1,358 water routes)
- **Aqueducts** - Roman aqueduct locations

**Settlements:**
- **Ancient Cities** - DARE settlements with Latin/modern names (major cities = larger markers)
- **Fortifications** - Roman military sites and fortifications

**Political:**
- **Roman Provinces** - Provincial boundary outlines
- **Modern Borders** - Current political boundaries

**Water Features:**
- **Rivers** - Ancient river network
- **Lakes** - Ancient lakes and bodies of water
- **Sailing Routes** - Mendeley research-based ancient Mediterranean shipping network (58 ports)

### Route Type Selector
When "Travel Line and Time" overlay is enabled, you can choose how the journey handles water crossings:
- **Land Only** - Routes only on the Roman Roads network (14,993 land segments + 834 river crossings)
- **Use Water** - Routes on both Roman Roads AND itiner-e Sea Lanes (524 sea segments) for optimal mixed land/water routing

**Graph-Based Routing:**
The system uses client-side Dijkstra shortest path on a preprocessed routing graph (11,031 nodes, 16,351 edges) built from the itiner-e Roman Roads dataset. This provides authentic ancient world routing without relying on external APIs.

**OSRM Fallback Routing:**
For locations outside the Roman road network (e.g., Mesopotamia, Arabia, Sinai Peninsula), the system automatically falls back to OSRM (Open Source Routing Machine) for modern road routing. Fallback routes are displayed with **dashed lines** to indicate they are modern approximations, not ancient Roman roads. A note in the travel info panel explains when fallback routes are used.

**Connector Legs:**
The straight-line distance from the user's location to the nearest road/port node is treated as land travel (walking to/from the network). This is semantically correct for historical travel.

**Travel Time Calculation:**
- Land segments use the selected transport mode speed (Walking: 4 km/h, Ox cart: 2 km/h, Pack animal: 4.5 km/h, Horse courier: 6 km/h)
- Sea segments use sailing speed of 4 knots (7.4 km/h)
- River segments are classified as land for travel time purposes

**Map Legend:**
When sea segments are included in a route, a legend appears in the travel info panel explaining line styles.

When "Use Water" is selected:
- Routes may include sea lane segments for optimal paths
- Water segments show an anchor icon (⚓) in the leg breakdown
- A summary shows land vs. sea distance and time breakdown

### Transport Mode Selector
Choose historical land travel speeds (applies to land portions):
- **Walking** - 4 km/h (default) - Standard foot travel
- **Ox cart** - 2 km/h - Slow freight transport
- **Pack animal** - 4.5 km/h - Mule or donkey caravan
- **Horse courier** - 6 km/h - Fast mounted messenger

The travel times displayed on the map dynamically recalculate when you change the transport mode or route type.

### Interactions
- Click/tap markers for detailed information
- **Mobile (≤768px):** Bottom drawer slides up, swipe down to close
- **Desktop:** Traditional popups
- **Instructions:** "?" button opens this guide in new window

---

## Final Validation Steps

Before providing URL to user, verify:

- [ ] URL starts with `https://mitchell360.com/map-maker/?`
- [ ] Every `~` has a location on left and label on right
- [ ] All pairs are separated by `|`
- [ ] No spaces in URL except encoded as `%20`
- [ ] Labels use `%0A` for line breaks
- [ ] URL is under 8000 characters

---

## Response Format to Users

When providing URLs to users, include:

1. **The complete working URL**
2. **Brief description** (e.g., "This map shows Paul's second missionary journey with 6 locations")
3. **Note about optional features** (e.g., "Toggle 'Travel Line and Time' overlay to see routes and estimated ancient travel times")

---

## Tips for LLMs

- ✅ **CRITICAL:** Always use `~` (tilde) to bind each location to its label
- ✅ **MANDATORY:** Every location must have a label bound to it with `~`
- ✅ Count mismatches are **impossible** with this format (location and label bound together)
- ✅ Always specify country/region with city names (e.g., `Rome, Italy` not `Rome`)
- ✅ Use rich 5-line label format for professional, information-rich popups
- ✅ First line of each label becomes the marker name displayed on map
- ✅ Lines 2-3 appear in gray as historical/modern context
- ✅ Line 5+ becomes the main description text in popup
- ✅ Use `%0A` for line breaks, `%0A%0A` for blank lines between sections
- ✅ Chronological locations are connected by walking paths in the order specified
- ✅ Reference locations are standalone and never connected to anything
- ✅ Keep URLs under 8000 characters for maximum compatibility
- ✅ Test your URL structure before providing to ensure all `~` separators are present

---

## Error Handling

- Invalid locations skipped (geocoding failure logged to console)
- Missing labels after `~` default to location name
- Empty parameters are ignored
- TBD labels display prominent placeholder warning
- Count mismatches **IMPOSSIBLE** with new format (fundamental architecture improvement)

---

**Documentation Standard:** This file follows the `llm.md` web standard for providing instructions to Large Language Models.
