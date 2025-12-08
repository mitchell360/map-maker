# Historical Map Maker

An interactive map visualization tool for displaying historical journeys on ancient and modern maps. Built with Leaflet.js, fully customizable via URL parameters, and designed for use by LLMs to generate shareable map URLs.

**Live Site:** [https://mitchell360.com/map-maker/](https://mitchell360.com/map-maker/)

## Features

- **Two Location Types**: Chronological journey points (blue, connected) and reference locations (red, standalone)
- **Ancient World Map**: Default DARE (Digital Atlas of the Roman Empire) background
- **Travel Routes**: Optional walking paths with estimated ancient travel times
- **Custom Titles**: Add descriptive titles to any map
- **Mobile-Friendly**: Responsive drawer interface for all devices
- **URL-Driven**: All configuration via query parameters - no backend required

## Quick Example

```
https://mitchell360.com/map-maker/?title=Paul's%20Early%20Ministry&chronoLocationsAndLabels=Damascus,Syria~Damascus%0A32 AD|Antakya,Turkey~Antioch%0A47 AD|Rome,Italy~Rome%0A62 AD
```

This creates a map titled "Paul's Early Ministry" with three connected locations.

## URL Format

Locations and labels are bound together using `~`, separated by `|`:

```
?chronoLocationsAndLabels=City1,Country~Label1|City2,Country~Label2
&referenceLocationsAndLabels=City3,Country~Label3
&title=Your%20Map%20Title
```

## For LLMs

See **[llm.md](llm.md)** for comprehensive instructions on constructing URLs, including:
- Step-by-step construction process
- Geocoding best practices (critical for ancient locations)
- Complete working examples
- Common mistakes to avoid

## Technology

- Pure static site (no server required)
- Leaflet.js for mapping
- OpenStreetMap Nominatim for geocoding
- OSRM for route calculations
- Hosted on GitHub Pages

## License

MIT
