// Creating the map object
let myMap = L.map("map", {
    center: [40.7128, -74.0059],
    zoom: 2.5

  });

// Adding the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

// use D3 to load the data from the nyc.geojson file
d3.json('companyLocations.geojson').then(
    (data)=>{
        console.log(data);


        L.geoJson(data,
            {
               // create the function to create popup 
               onEachFeature: function(feature, layer){
                // Giving each feature a popup with information that's relevant to it
                layer.bindPopup("<center><h2>" + feature.properties.Company + "<br>" + feature.properties.Ticker + "<br>" + feature.properties.Change + "</h2> <hr> <h3>");
                //set mouse events to change map styling when company location points are clicked
                 layer.on({
                                     mouseover: function(event)
                    {
                        // reference the item (layer) that triggers the event
                        layer = event.target;
                        // use setStyle to update the fillOpacity style property
                        //layer.setStyle({
                            //fillOpacity: 0.9,
                            //weight: 5
                        //});
                    },
                     mouseout: function(event)
                    {
                        // reference the item (layer) that triggers the event
                        //layer = event.target;
                        // use setStyle to update the fillOpacity style property
                        //layer.setStyle({
                           // fillOpacity: 0.6,
                            //weight: 2
                        //});
                    }
                });
               }
            }
        ).addTo(myMap);
    }
);