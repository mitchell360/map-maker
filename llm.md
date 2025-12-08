# Historical Map URL Construction Instructions for LLMs

**Service:** Historical Map Visualization  
**Base URL:** `https://mitchell360.com/map-maker/`  
**Last Updated:** 2025-10-28

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

The map uses OpenStreetMap's geocoding API, which works with **modern place names only**.

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

**Default:** If no title parameter is provided, displays `"Paul's Missionary Journeys"`

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

**Option A: Without Custom Title (uses default "Paul's Missionary Journeys"):**
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

**Displays:** Two blue markers connected by a walking path (default title: "Paul's Missionary Journeys")

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
https://mitchell360.com/map-maker/?title=The%20Seven%20Churches%20of%20Revelation&chronoLocationsAndLabels=Selcuk,Turkey~Ephesus%0ARevelation 2:1-7: Ephesus, Asia Minor%0A2025 AD: Near Selçuk, Türkiye%0A%0AThe church that lost its first love|Izmir,Turkey~Smyrna%0ARevelation 2:8-11: Smyrna, Asia Minor%0A2025 AD: İzmir, Türkiye%0A%0AThe suffering church|Bergama,Turkey~Pergamum%0ARevelation 2:12-17: Pergamum, Asia Minor%0A2025 AD: Bergama, Türkiye%0A%0AWhere Satan's throne is|Akhisar,Turkey~Thyatira%0ARevelation 2:18-29: Thyatira, Asia Minor%0A2025 AD: Akhisar, Türkiye%0A%0AThe compromising church|Salihli,Turkey~Sardis%0ARevelation 3:1-6: Sardis, Asia Minor%0A2025 AD: Near Salihli, Türkiye%0A%0AThe dead church|Alasehir,Turkey~Philadelphia%0ARevelation 3:7-13: Philadelphia, Asia Minor%0A2025 AD: Alaşehir, Türkiye%0A%0AThe faithful church|Denizli,Turkey~Laodicea%0ARevelation 3:14-22: Laodicea, Asia Minor%0A2025 AD: Near Denizli, Türkiye%0A%0AThe lukewarm church
```

**Displays:** Seven churches in order with connected path and descriptive title

**⚠️ Important Note:** This example uses **modern city names** in the location field (e.g., `Alasehir,Turkey` not `Philadelphia,Turkey`) to ensure accurate geocoding. Ancient names are shown in the labels.

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

### Base Maps
- **Ancient World (DARE)** - Default historical map
- **Modern Clean** - CartoDB Positron
- **Modern Detailed** - OpenStreetMap

### Overlays (Toggle in layer control)
- **Country Borders** - Political boundaries
- **Travel Line and Time** - Color-coded walking routes with travel time estimates

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
