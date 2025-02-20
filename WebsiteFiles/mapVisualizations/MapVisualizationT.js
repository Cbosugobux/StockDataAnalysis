// ✅ Ensure script loads
console.log("✅ MapVisualizationT.js Loaded");

// Initialize Leaflet Map
var mapT = L.map('mapT').setView([37.8, -96], 4); // USA centered

// Add OpenStreetMap Tile Layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(mapT);

// Load Company Locations
fetch('companyLocations.geojson')
    .then(response => response.json())
    .then(companyData => {
        console.log("✅ Company Locations Loaded", companyData);

        // Load Trump Stock Data
        fetch('../../Data/Trump.json') // Corrected path
            .then(response => response.json())
            .then(stockData => {
                console.log("✅ Trump Stock Data Loaded", stockData);

                // Match Stock Data to Locations
                companyData.features.forEach(feature => {
                    let companyName = feature.properties.name;
                    let stockInfo = stockData[companyName]; // Match stock performance

                    if (stockInfo) {
                        let change = stockInfo.change; // % Change
                        let color = change > 0 ? "green" : "red"; // Color based on performance

                        // Create Marker
                        L.circleMarker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], {
                            color: color,
                            radius: Math.abs(change) / 2, // Scale marker size
                            fillOpacity: 0.7
                        })
                        .bindPopup(`<strong>${companyName}</strong><br>Stock Change: ${change}%`)
                        .addTo(mapT);
                    }
                });
            })
            .catch(error => console.error("❌ Error loading Trump Stock Data:", error));
    })
    .catch(error => console.error("❌ Error loading GeoJSON Data:", error));
