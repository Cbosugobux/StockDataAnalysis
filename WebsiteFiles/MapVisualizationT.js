// Creating the map object
let myMap = L.map("mapT", {
    center: [25, 10],
    zoom: 1.5
});

// Adding the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

// Load the GeoJSON file
d3.json('companyLocations.geojson').then(function (data) {

    function dataColor(TrumpChange) {
        return TrumpChange < 0 ? "tomato" : "limegreen";
    }

    function readiusSize(TrumpChange) {
        return TrumpChange === 0 ? 1 : Math.abs(TrumpChange) * 5;
    }

    function dataStyle(feature) {
        return {
            opacity: 0.5,
            fillOpacity: 0.5,
            fillColor: dataColor(feature.properties.TrumpChange),
            radius: readiusSize(feature.properties.TrumpChange),
            weight: 0.5,
            stroke: true
        };
    }

    // Function to show hover popup
    function highlightFeature(event) {
        let layer = event.target;

        // Increase opacity on hover
        layer.setStyle({
            opacity: .75,
            fillOpacity: .75
        });

        // Extract details from the GeoJSON properties
        let company = layer.feature.properties.Company;
        let ticker = layer.feature.properties.Ticker;
        let stockChange = layer.feature.properties.TrumpChange;
        let city = layer.feature.properties.City || "Unknown";
        let state = layer.feature.properties.State || "Unknown";
        let country = layer.feature.properties.Country || "Unknown";

        // Define popup content
        let popupContent = `
            <center>
                <h2>${company} - ${ticker}</h2>
                <hr>
                <h3>Stock Change: ${stockChange}</h3>
                <p><b>Location:</b> ${city}, ${state}, ${country}</p>
            </center>`;

        // Open popup with the new content
        layer.bindPopup(popupContent).openPopup();
    }

    // Function to reset style and close popup on mouseout
    function resetHighlight(event) {
        let layer = event.target;
        layer.setStyle({
            opacity: 0.5,
            fillOpacity: 0.5
        });
        layer.closePopup();
    }

    // Add the GeoJSON data
    L.geoJson(data, {
        pointToLayer: function (feature, latLng) {
            return L.circleMarker(latLng);
        },
        style: dataStyle,
        onEachFeature: function (feature, layer) {
            // Default popup when clicking a marker
            let defaultPopup = `
                <center>
                    <h2>${feature.properties.Company} - ${feature.properties.Ticker}</h2>
                    <hr>
                    <h3>Stock Change: ${feature.properties.TrumpChange}</h3>
                </center>`;

            layer.bindPopup(defaultPopup);

            // Add mouseover event to show the hover popup with City, State, and Country
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight
            });
        }
    }).addTo(myMap);
});