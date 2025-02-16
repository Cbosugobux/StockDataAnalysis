// Creating the map object
let myMapB = L.map("mapB", {
    center: [ 25, 10],
    zoom: 1.5

  });

// Adding the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMapB);

//create variable for the company locations
let stockchangelayer = new L.layerGroup();

// use D3 to load the data from the nyc.geojson file
d3.json('companyLocations.geojson').then(
    function(data){
    
        function dataColor(BidenChange){
            if (BidenChange < 0)
                return "red";

            else if(BidenChange >0)
                return "green";
        }

        //makea function to determine the size of the radius
        function readiusSize(BidenChange) {
            if(BidenChange == 0)
                return 1
            
            else
                return Math.abs(BidenChange) * 5; // scales the difference between earthquake magnitudes
        }

        //add on to the sytle for each data point
        function dataStyle(feature)
        {
            return{
                opacity: .5,
                fillOpacity: .5,
                fillColor: dataColor(feature.properties.BidenChange),
                radius: readiusSize(feature.properties.BidenChange),
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
            layer.bindPopup("<center><h2>" + feature.properties.Company + "<br>" + feature.properties.Ticker + "<br>" + "Stock Change: " + feature.properties.BidenChange + "</h2> <hr> <h3>");
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

            
        ).addTo(myMapB);
    }
);