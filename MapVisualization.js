// Creating the map object
let myMap = L.map("map", {
    center: [40.7128, -74.0059],
    zoom: 15
  });

// Adding the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

// use D3 to load the data from the nyc.geojson file
d3.json('companyLocation.geojson').then(
    (data)=>{
        console.log(data);

        // make a quick outline of the boroughs and neighborhoods 
        //L.geoJson(data).addTo(myMap);

        // use borough attribute to color the borough using this inline function
        
///        function boroughColor(borough)
   ///     {
      ///      // use borough name as a parameter to choose one of the following colors
         ///   if (borough == "Brooklyn") return "yellow";
            ///else if (borough == "Bronx") return "red";
            ///else if (borough == "Manhattan") return "orange";
            ///else if (borough == "Queens") return "green";
            ///else if (borough == "Staten Island") return "purple";
            ///else return "black";
        ///}

        // expand the properties of L.geoJson to style the boroughs
        L.geoJson(data,
            {
                // use the style attribute to go and add some different styling to the outline
                /*style: {
                    color: "black",
                    fillColor: "pink",
                    fillOpacity: 0.6,
                    weight: 2
                }*/
                style: function(feature)
                {
                    return {
                        color: "black",
                        fillColor: "blue",
                        fillOpacity: 0.6,
                        weight: 2
                    }
                },
                // onEachFeature property, can be used to tell what happens when we interact
                // with the drawn out portions of the map (the boroughs and neighborhoods) 
               onEachFeature: function(feature, layer){
                // Giving each feature a popup with information that's relevant to it
                layer.bindPopup("<center><h2>" + feature.properties.neighborhood + "</h2> <hr> <h3>");
                //set mouse events to change map styling when neighobrhoods are hovered
                 layer.on({
                                     mouseover: function(event)
                    {
                        // reference the item (layer) that triggers the event
                        layer = event.target;
                        // use setStyle to update the fillOpacity style property
                        layer.setStyle({
                            fillOpacity: 0.9,
                            weight: 5
                        });
                    },
                     mouseout: function(event)
                    {
                        // reference the item (layer) that triggers the event
                        layer = event.target;
                        // use setStyle to update the fillOpacity style property
                        layer.setStyle({
                            fillOpacity: 0.6,
                            weight: 2
                        });
                    }
                });
               }
            }
        ).addTo(myMap);
    }
);