var base_url = "";
var found = window.location.search.match(/s3bucket=(?<bucket>.*)/);
if (found) {
    var bucket = found.groups.bucket;
    // TODO: make the AWS region variable
    base_url = "https://" + bucket + ".s3.us-east-2.amazonaws.com/";
}
var fetch_json = function (url) {
    return fetch(base_url + url)
};

var popup;
var arr=[[-1, '#000000'],[1, '#1a9850'],[20, '#ffffb2'],[200, '#fd8d3c'],[1000, '#fc4e2a'],[20000, '#bd0026'],[30000, '#800026']];   
var arr2=[[1, 0.1], [100, 0.2],[200, 0.7],[500, 1],[1000, 1],[2000, 1],[2500, 1],[3000, 1],[50000, 1]];  
var comms=["All",0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21];  
var data3=[];    

    var data0=[];
            fetch_json('output/classification/classification_ids_counties2.json').then(res => res.json())
.then(data0 => { 
             // console.log(data0);  
         var cols={"green":0,"yellow":0.1,"orange":0.4,"red":1}       
                var ids=data0.map(function(d){return d.id.toString().substring(3)});
         //  console.log(ids);
        fetch_json('counties5.json').then(res => res.json())
.then(data => {  
 
            for (var i=0; i<data["features"].length; i++) {
                data["features"][i]["id"]=data["features"][i]["properties"]["GEOID"];
                if (ids.indexOf(data["features"][i]["properties"]["GEOID"])>-1) {
                    
                data["features"][i]["properties"]["v"]=data0[ids.indexOf(data["features"][i]["properties"]["GEOID"])]["max"];
                } else {
                  //  console.log(data["features"][i]["properties"]);
                    data["features"][i]["properties"]["v"]=-1;
                    
                    
                    
                    
                }
            }
            var hoveredStateId = null;

	mapboxgl.accessToken = 'pk.eyJ1Ijoib2J1Y2hlbCIsImEiOiJjamhqZTZsOWkwN25iM2Fxd282N2FlZDVqIn0.bkOU5gAio8eKnmKHlntJsA';
var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/light-v9',
zoom: 3,
     attributionControl: false,
center: [-82.447303,37.753574]
});
         
map.addControl(new mapboxgl.NavigationControl(), 'top-left');       
map.addControl(new mapboxgl.FullscreenControl(), 'bottom-left');
map.on('load', function() {    

  
fetch_json('states5.json').then(res => res.json())
.then(data8 => {   
     // define layer names
        var layers = [
            '<b>New cases past 14 days:</b>',
            ' ',
             'None',
          '1-20',
          '21-200',
          '201-1,000',
          '1,001-20,000',
            '20,000-30,000'
        ];

        var colors = [
            '',
                '',
                '#6A8A88',
          '#1a9850',
          '#ffffb2',
          '#fd8d3c',
          '#bd0026',
          '#800026'
        ];

        // create legend
        for (i = 0; i < layers.length; i++) {
          var layer = layers[i];
          var color = colors[i];
          var item = document.createElement('div');
          var key = document.createElement('span');
          key.className = 'legend-key';
          key.style.backgroundColor = color;
            
 key.style.borderStyle = "ridge";
          var value = document.createElement('span');
          value.innerHTML = layer;
            if (i!=0 && color !="") {
          item.appendChild(key);
            }
          item.appendChild(value);
          legend.appendChild(item);
        }
    
     var value3 = document.createElement('span');
    value3.innerHTML = "&nbsp;";
    var item3 = document.createElement('div');
     item3.appendChild(value3);
          legend.appendChild(item3);
    
    
        var value2 = document.createElement('span');
   

    value2.innerHTML = "Updated: "+data0[0]["date"];
     value2.style.textAlign="center !important";
    value2.style.margin="auto";
    var item2 = document.createElement('div');
     item2.appendChild(value2);
          legend.appendChild(item2);
    
    
    
    
map.addSource('ethnicity', {
type: 'geojson',
'data': data    
});
    
    map.addSource('states', {
type: 'geojson',
'data': data8    
});
      
      map.addLayer({
'id': 'place_data0',
'type': 'fill',
'source': 'ethnicity',
      /*
className: {
property: "country"
},*/
'paint': {
'fill-color': {
property: "v",
stops: arr
},
'fill-outline-color': 'black',
'fill-opacity': [
'case',
['boolean', ['feature-state', 'hover'], false],
1,
0.5
]/*,     
'fill-opacity': {
property: "value",
stops: arr2
}*/
},
'filter': ['==', '$type', 'Polygon']
});  
    
     map.addLayer({
'id': 'states',
'type': 'line',
'source': 'states',
'layout': {
'line-join': 'round',
'line-cap': 'round'
},
'paint': {
'line-color': '#000000',
'line-width': 1
}
});    
    
map.on('mousemove', 'place_data0', function(e) {
    if (typeof popup=="object") popup.remove();
if (e.features.length > 0) {
   
 
if (hoveredStateId) {
map.setFeatureState(
{ source: 'ethnicity', id: hoveredStateId },
{ hover: false }
);
}
    var coordinates = e.features[0].geometry.coordinates[0][0].slice();
    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
}
//hoveredStateId = e.features[0].properties.id;
hoveredStateId = e.features[0].id;    
popup=new mapboxgl.Popup()
.setLngLat(e.lngLat)
.setHTML(e.features[0].properties.NAME+": "+e.features[0].properties.v)
.addTo(map);

   // console.log(e.features[0].properties);
map.setFeatureState(
{ source: 'ethnicity', id: hoveredStateId },
{ hover: true }
);
}
});

// When the mouse leaves the state-fill layer, update the feature state of the
// previously hovered feature.
map.on('mouseleave', 'place_data0', function() {


if (hoveredStateId) {
map.setFeatureState(
{ source: 'ethnicity', id: hoveredStateId },
{ hover: false }
);
}
hoveredStateId = null;
    
 
});
    
    
    /*
    
    
    map.on('mouseenter', 'places', function(e) {

var coordinates = e.features[0].geometry.coordinates[0][0];
var description = e.features[0].properties.NAMELSAD;

popup
.setLngLat(coordinates)
.setHTML(description)
.addTo(map);
});
 
map.on('mouseleave', 'places', function() {

popup.remove();
});*/
      });
           });
     });
/*
var map2 = new mapboxgl.Map({
container: 'map2',
style: 'mapbox://styles/mapbox/light-v10',
zoom: 1,
center: [-22.447303, 37.753574]
});    
    var zoomCurrent = 1;
    var zoomThreshold = 5;
    var 
    zoomPrevious = 'com1_color'; 
var stateLegendEl = document.getElementById('state-legend');
    */
    
    
    
     /*   
data3=data1;    
data0=data; 
map.on('load', function() {

map.addSource('ethnicity', {
type: 'geojson',

'data': data    
});
    

map.addLayer({
'id': 'population',
'type': 'circle',
'source': 'ethnicity',
//'source-layer': 'sf2010',
'paint': {
'circle-radius':3,
'circle-color': ['get', 'com1_color']
}
});
    

});     
        
        map2.on('load', function() {
   
            
   
            
            

map2.addSource('ethnicity', {
type: 'geojson',

'data': data    
});
    

map2.addLayer({
'id': 'population',
'type': 'circle',
'source': 'ethnicity',

'paint': {
'circle-radius':3,    
'circle-color': ['get', 'com0_color']
}
});
   
            
   map2.addSource('places', {
'type': 'geojson',
'data': data3
});

});     
});   
        
   */     
        
        

         });

        /*
    var data10 = [{"color":"#1a9850","value":1}, {"color":"#ffffb2","value":20},{"color":"#fd8d3c","value":200},
    var data10 = [{"color":"#1a9850","value":1}, {"color":"#ffffb2","value":20},{"color":"#fd8d3c","value":200},
       {"color":"'#fc4e2a","value":1000},
                {"color":"#bd0026","value":20000},
                {"color":"#800026","value":30000}];
    var extent = d3.extent(data10, d => d.value);
    
    var padding = 9;
    var width = 220;
    var innerWidth = width - (padding * 2);
    var barHeight = 8;
    var height = 28;

    var xScale = d3.scaleLinear()
        .range([0, innerWidth])
        .domain(extent);

    var xTicks = data10.filter(f => f.value % 1 === 0).map(d => d.value);

    var xAxis = d3.axisBottom(xScale)
        .tickSize(barHeight * 2)
        .tickValues(xTicks);

    var svg = d3.select("#state-legend0").append("svg").attr("width", width).attr("height", height);
    var g = svg.append("g").attr("transform", "translate(" + padding + ", 0)");

    var defs = svg.append("defs");
    var linearGradient = defs.append("linearGradient").attr("id", "myGradient");
    linearGradient.selectAll("stop")
        .data(data10)
      .enter().append("stop")
        .attr("offset", d => ((d.value - extent[0]) / (extent[1] - extent[0]) * 100) + "%")
        .attr("stop-color", d => d.color);

    g.append("rect")
        .attr("width", innerWidth)
        .attr("height", barHeight)
        .style("fill", "url(#myGradient)");

    g.append("g")
        .call(xAxis);
      //.select(".domain").remove();
    
function change_map(e){
    
    map.removeLayer('population');
    map.removeSource('ethnicity');
       // map2.removeLayer('places');
    //map2.removeLayer('place_data');
    map2.removeLayer('population');
    map2.removeSource('ethnicity');
    
  var data2={}
  data2["type"]="FeatureCollection";
  data2["features"]=[];
    
for (var i=0; i<data0["features"].length; i++) {
    
    if (data0["features"][i]["properties"]["com1"]==document.getElementById("mySelect").value) {
    data2["features"].push(data0["features"][i]);
    }
}    
    
    
    map.addSource('ethnicity', {
type: 'geojson',
'data': data2   
});
    
    
    map.addLayer({
'id': 'population',
'type': 'circle',
'source': 'ethnicity',
//'source-layer': 'sf2010',
'paint': {
    'circle-radius':2,
         //   'circle-stroke-color': "black",//['get', 'com1_color'],
   // 'circle-stroke-width':0.5,
'circle-color': ['get', 'com0_color'],
     'circle-opacity': 0.7
}
});
    
    map2.addSource('ethnicity', {
type: 'geojson',

'data': data2   
});
    

    
     map2.addLayer({
'id': 'population',
'type': 'circle',
'source': 'ethnicity',
//'source-layer': 'sf2010',
'paint': {
    'circle-radius':2,
 // 'circle-stroke-color': "black",//['get', 'com0_color'],
  //  'circle-stroke-width': 0.5,
'circle-color': ['get', 'com0_color'],
     'circle-opacity': 0.7
}
});
    
    
    
}    */
//document.getElementById("mySelect").addEventListener("click",change_map);  
