// ✅ Ensure script loads
console.log("✅ MapVisualizationB.js Loaded");

// Initialize Leaflet Map
var mapB = L.map('mapB').setView([20, 10], 2); // Adjusted to fit global view

// Add OpenStreetMap Tile Layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(mapB);

// ✅ Embed `companyLocations.geojson` with 5 U.S. + 5 Foreign Companies
var companyData = {
    "type": "FeatureCollection",
    "features": [
        // 🏢 U.S. Companies (Domestic)
        { "type": "Feature", "properties": { "name": "Apple" }, "geometry": { "type": "Point", "coordinates": [-122.032, 37.331] } },
        { "type": "Feature", "properties": { "name": "Microsoft" }, "geometry": { "type": "Point", "coordinates": [-122.1245, 47.6401] } },
        { "type": "Feature", "properties": { "name": "Amazon" }, "geometry": { "type": "Point", "coordinates": [-122.3351, 47.608] } },
        { "type": "Feature", "properties": { "name": "Google" }, "geometry": { "type": "Point", "coordinates": [-122.084, 37.422] } },
        { "type": "Feature", "properties": { "name": "Nvidia" }, "geometry": { "type": "Point", "coordinates": [-121.995, 37.370] } },

        // 🌍 Foreign Companies
        { "type": "Feature", "properties": { "name": "Alibaba" }, "geometry": { "type": "Point", "coordinates": [120.1551, 30.2741] } }, // Hangzhou, China
        { "type": "Feature", "properties": { "name": "Tencent" }, "geometry": { "type": "Point", "coordinates": [113.2644, 23.1291] } }, // Shenzhen, China
        { "type": "Feature", "properties": { "name": "TSMC" }, "geometry": { "type": "Point", "coordinates": [121.5654, 25.033] } }, // Taipei, Taiwan
        { "type": "Feature", "properties": { "name": "ASML" }, "geometry": { "type": "Point", "coordinates": [5.475, 51.4408] } }, // Veldhoven, Netherlands
        { "type": "Feature", "properties": { "name": "SAP" }, "geometry": { "type": "Point", "coordinates": [8.6512, 49.4875] } } // Walldorf, Germany
    ]
};

// ✅ Embed `Biden.json` with stock performance data for these 10 companies
var stockData = {
    "Apple": { "change": 15.2 },
    "Microsoft": { "change": -3.4 },
    "Amazon": { "change": 10.8 },
    "Google": { "change": 7.1 },
    "Nvidia": { "change": 30.4 },
    "Alibaba": { "change": -2.9 },
    "Tencent": { "change": -5.6 },
    "TSMC": { "change": 15.9 },
    "ASML": { "change": 8.4 },
    "SAP": { "change": 2.1 }
};

// ✅ Display Markers on Map
companyData.features.forEach(feature => {
    let companyName = feature.properties.name;
    let stockInfo = stockData[companyName]; // Match stock performance

    if (stockInfo) {
        let change = stockInfo.change; // % Change
        let color = change > 0 ? "green" : "red"; // Green for growth, red for decline

        // Create Marker
        L.circleMarker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], {
            color: color,
            radius: Math.max(5, Math.abs(change) / 2), // Ensures markers are visible
            fillOpacity: 0.7
        })
        .bindPopup(`<h3>${companyName}</h3>
                    <p><strong>Stock Change:</strong> ${change}%</p>
                    <p>Under Biden</p>`)
        .addTo(mapB);
    }
});

console.log("✅ Map Markers Added Successfully for Biden Data");
