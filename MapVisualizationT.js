// Creating the map object
let myMapT = L.map("mapT", {
    center: [ 25.417039000001637, 10.404563739044704],
    zoom: 1.5

  });

// Adding the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMapT);

//create variable for the company locations
let stockchangelayer = new L.layerGroup();

// use D3 to load the data from the nyc.geojson file
d3.json('companyLocations.geojson').then(
    function(data){
    
        function dataColor(TrumpChange){
            if (TrumpChange < 0)
                return "red";

            else if(TrumpChange >0)
                return "green";
        }

        //makea function to determine the size of the radius
        function readiusSize(TrumpChange){
            if(TrumpChange == 0)
                return 1
            
            else
                return TrumpChange * 5; // scales the difference between earthquake magnitudes
        }

        //add on to the sytle for each data point
        function dataStyle(feature)
        {
            return{
                opacity: .5,
                fillOpacity: .5,
                fillColor: dataColor(feature.properties.TrumpChange),
                radius: readiusSize(feature.properties.TrumpChange),
                weight: 0.5,
                stroke: true
            }
        }
                //add the GeoJson Data
        L.geoJson(data, {
                    //make each feature a marker that is on the map, each marker is a circle
            pointToLayer: function(feature, latLng){
                return L.circleMarker(latLng);
                },
        
                    //set style for each marker
            style: dataStyle, //calls the dataStyle function and passes in the earthquake data
        

        
            
               // create the function to create popup 
            onEachFeature: function(feature, layer){
                // Giving each feature a popup with information that's relevant to it
            layer.bindPopup("<center><h2>" + feature.properties.Company + "<br>" + feature.properties.Ticker + "<br>" + "Stock Change: " + feature.properties.TrumpChange + "</h2> <hr> <h3>");
                //set mouse events to change map styling when company location points are clicked
                layer.on({
                                mouseover: function(event)
                    {
                        // reference the item (layer) that triggers the event
                        layer = event.target;
                        
                    }
                     
                });
               }
            }

            
        ).addTo(myMapT);
    }
);