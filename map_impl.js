var popup;
    
    
    
var arr=[[-1, '#000000'],[0, '#1a9850'],[0.1, '#fed976'],[0.4, '#fd8d3c'],[0.8, '#bd0026'],[1, '#800026']];   
     var arr2=[[1, 0.1], [100, 0.2],[200, 0.7],[500, 1],[1000, 1],[2000, 1],[2500, 1],[3000, 1],[50000, 1]];  
var comms=["All",0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21];  
var data3=[];    

    var data0=[];
            fetch('output/classification/classification_ids_counties2.json').then(res => res.json()) 
.then(data0 => { 
             // console.log(data0);  
         var cols={"green":0,"yellow":0.1,"orange":0.4,"red":1}       
                var ids=[];
                
                data0.map(function(d,i){if (d.id.toString().length>3) {ids.push(d.id.toString().substr(3)) }else 
                                                                     {ids.push(d.id.toString())}
                                                                     
                                                                     });
           //console.log(ids);
        fetch('counties_clipped.json').then(res => res.json()) 
.then(data => {  
 var data2={"type":"FeatureCollection"};
    data2["features"]=[];        
            
            for (var i=0; i<data["features"].length; i++) {
                data["features"][i]["id"]=data["features"][i]["properties"]["GEOID"].toString();
                // if (data["features"][i]["properties"]["STATEFP"]!="72") {
                if (ids.indexOf(data["features"][i]["properties"]["GEOID"])>-1) {
                      data["features"][i]["properties"]["c"]=data0[ids.indexOf(data["features"][i]["properties"]["GEOID"])]["c"];
                    data["features"][i]["properties"]["max"]=data0[ids.indexOf(data["features"][i]["properties"]["GEOID"])]["max"];
                     data["features"][i]["properties"]["max1"]=Math.log(data0[ids.indexOf(data["features"][i]["properties"]["GEOID"])]["max"]+1)*0.5;
                data["features"][i]["properties"]["v"]=cols[data0[ids.indexOf(data["features"][i]["properties"]["GEOID"])]["c"]];
                } else {

                    data["features"][i]["properties"]["v"]=-1;
                    data["features"][i]["properties"]["max"]=0;
                     data["features"][i]["properties"]["max1"]=Math.log(1)*0.5;
                }
               // if (data["features"][i]["id"]!="630") {
                data2["features"].push({"type": "Feature", "geometry": {"type": "Point", "coordinates":[Number(data["features"][i]["properties"]["INTPTLON"]),Number(data["features"][i]["properties"]["INTPTLAT"])]},"properties":data["features"][i]["properties"]});
            //    }
                // }
            }
            
            

            var hoveredStateId = null;
//pk.eyJ1Ijoib2J1Y2hlbCIsImEiOiJjamhqZTZsOWkwN25iM2Fxd282N2FlZDVqIn0.bkOU5gAio8eKnmKHlntJsA
	mapboxgl.accessToken = 'pk.eyJ1Ijoib2J1Y2hlbCIsImEiOiJmOWQ2MzQxNmE0M2Y3YmVjNzA2NmM2MGQzYTIwYmQ3OCJ9.psxJSN8q9n2-HfFGoIUNJA';
var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/light-v10',
zoom: 3,
    attributionControl: false,
center: [-82.447303,37.753574]
});
     
map.addControl(new mapboxgl.NavigationControl(), 'top-left');      
map.addControl(new mapboxgl.FullscreenControl());
fetch('states.json').then(res => res.json()) 
.then(data8 => {             

map.on('load', function() {    

        var layers = [
          '<img width="20px" height="20px" src="green.png"> : Daily new cases under control',
          '<img width="20px" height="20px" src="yellow.png"> : Daily new cases almost under control',
          '<img width="20px" height="20px" src="orange.png"> : Daily new cases are high, but falling or constant',
          '<img width="20px" height="20px" src="red.png"> : Daily new cases are high and spreading rapidly'
        ];

        var colors = [
          '#1a9850',
          '#ffffb2',
          '#fd8d3c',
          '#bd0026'
        //  '#800026'
        ];
    
    var value = document.createElement('span');
          value.innerHTML = '<b>Legend</b>:';
var item = document.createElement('div');
     item.appendChild(value);
          legend.appendChild(item);
    

        for (i = 0; i < layers.length; i++) {
          var layer = layers[i];
          var color = colors[i];
          var item = document.createElement('div');
          var key = document.createElement('span');
          key.className = 'legend-key';
          key.style.backgroundColor = color;

          var value = document.createElement('span');
          value.innerHTML = layer;
          item.appendChild(key);
          item.appendChild(value);
          legend.appendChild(item);
        }
  var value = document.createElement('span');
          value.innerHTML = '<svg width="2" height="2">  <circle cx="1" cy="1" r="0.8" fill="none" stroke="black"/></svg> <svg width="10" height="10">  <circle cx="5" cy="5" r="4.5" fill="none" stroke="black"/></svg> <svg width="15" height="15"><circle cx="7.5" cy="7.5" r="7" fill="none" stroke="black"/></svg> - Numbers of cases in the past 2 weeks';
var item = document.createElement('div');
     item.appendChild(value);
          legend.appendChild(item);
    
    
map.addSource('ethnicity', {
type: 'geojson',
'data': data    
});
    map.addSource('states', {
type: 'geojson',
'data': data8    
});
   map.addSource('ethnicity2', {
type: 'geojson',
'data': data2    
});
     map.addLayer({
'id': 'place_data0',
'type': 'fill',
'source': 'ethnicity',

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
]
},
'filter': ['==', '$type', 'Polygon']
});  
    
    
     map.addLayer({
'id': 'population',
'type': 'circle',
'source': 'ethnicity2',
'paint': {
    'circle-radius':['get', 'max1'],
  'circle-stroke-color': '#000000',
    'circle-stroke-width': 0.5,
'circle-color': "grey",
     'circle-opacity': 0.1
}
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
map.on('click', 'place_data0', function(e) {
    if (typeof popup=="object") popup.remove();

   
 hoveredStateId = null;

    var coordinates = e.features[0].geometry.coordinates[0][0].slice();
    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
}
    
     var htm=e.features[0].properties.NAMELSAD+": "+e.features[0].properties.max+"<br>";
    
    hoveredStateId = e.features[0].id;    
    var lats=e.lngLat;
    
if (e.features[0].properties["c"]=="yellow") {
    var color="#fed976";
} else if (e.features[0].properties["c"]=="green") {
 var color="#1a9850";
} else if (e.features[0].properties["c"]=="red") {
 var color="#800026";
} else 


{
    var color=e.features[0].properties["c"];
}

    document.getElementById("plot").innerHTML="";
    
    if (e.features[0].id.toString().length==4){
        var num="0"+e.features[0].id.toString();
        
    } else {
    var num=e.features[0].id.toString();
    }
    
    if (["630","16","316","580","850"].indexOf(num)>-1) {
        
        var url='output/classification/data_counties_'+num+'.json';
    } else {
        
        var url='output/classification/data_counties_840'+num+'.json';
    }
    
    
  fetch(url).then(res => res.json()) 
.then(data7 => {      
        draw_plot(data7,color);

popup=new mapboxgl.Popup()
.setLngLat(lats)
.setHTML(htm)
.addTo(map);
      
   /* document.getElementsByClassName("mapboxgl-popup-close-button")[0].on('click', function(e) {
       //  alert(e);

turn_off();
 });*/
      
      
      
      });  
      
  });

});


    
   
     });
      
     });


         });
    
        
    

    
function draw_plot(data,color) {
    document.getElementById("plot").style.visibility="visible";
   document.getElementById("features").style.visibility="visible";
    //console.log(data);
   // console.log(data["dates"][0].split("/"));
    //"original_values", time, dates
    var data110=[];
    
    for (var i=0; i<data["dates"].length; i++) {
        if (data["value"][i]>=0){
            var val=data["value"][i];
        } else {
            var val=0;
        }
        var temp={"date":new Date(2020,Number(data["dates"][i].split("/")[0])-1,Number(data["dates"][i].split("/")[1])),"value":val};
        data110.push(temp);
    }
    
 var data10=[];
    
    for (var i=1; i<data["time"].length; i++) {
        if (data["original_values"][i]>=0){
            var val=data["original_values"][i];
        } else {
            var val=0;
        }
        var temp={"date":new Date(2020,Number(data["time"][i].split("/")[0])-1,Number(data["time"][i].split("/")[1])),"value":val};
        data10.push(temp);
    }
   //console.log(data110.map(function(d){ return d.value}),data10.map(function(d){ return d.value}));
    var margin = {top: 25, right: 20, bottom: 20, left: 35},
    width = 250 - margin.left - margin.right,
    height = window.innerHeight*0.3 - margin.top - margin.bottom;
    
    var svg = d3.select("#plot")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    var defs = svg.append("defs");


var dropShadowFilter = defs.append('svg:filter')
  .attr('id', 'drop-shadow')
  .attr('filterUnits', "userSpaceOnUse")
  .attr('width', '250%')
  .attr('height', '250%');
dropShadowFilter.append('svg:feGaussianBlur')
  .attr('in', 'SourceGraphic')
  .attr('stdDeviation', 2)
  .attr('result', 'blur-out');
dropShadowFilter.append('svg:feColorMatrix')
  .attr('in', 'blur-out')
  .attr('type', 'hueRotate')
  .attr('values', 180)
  .attr('result', 'color-out');
dropShadowFilter.append('svg:feOffset')
  .attr('in', 'color-out')
  .attr('dx', 3)
  .attr('dy', 3)
  .attr('result', 'the-shadow');
dropShadowFilter.append('svg:feBlend')
  .attr('in', 'SourceGraphic')
  .attr('in2', 'the-shadow')
  .attr('mode', 'normal');
    
    // Add X axis --> it is a date format
    var x = d3.scaleTime()
      .domain(d3.extent(data10, function(d) { return d.date; }))
      .range([ 0, width ]);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(5));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0,d3.max(data10, function(d) { return +d.value; })])
      .range([ height, 0]);
    svg.append("g")
      .call(d3.axisLeft(y).ticks(5));

    
  
      var path1 = svg.append("path")
      .datum(data10)
      .attr("fill", "none")
      .attr("stroke", "grey")
      .attr("stroke-width", 0.5)
      .attr("d", d3.line()
        .x(function(d) { return x(d.date) })
        .y(function(d) { return y(d.value) })
            //.curve(d3.curveNatural)
        );
       // .style("filter", "url(#drop-shadow)");
  
// Add the line
      var path = svg.append("path")
      .datum(data110)

      .attr("fill", "none")
      .attr("stroke", color)
      .attr("stroke-width", 3)
      .attr("d", d3.line()
        .x(function(d) { return x(d.date) })
        .y(function(d) { return y(d.value) })
           // .curve(d3.curveNatural)
        );
       // .style("filter", "url(#drop-shadow)");
    
    var curtain = svg.append('rect')
 .attr('x', -1 * width)
 .attr('y', -1 * height)
 .attr('height', height+20)
 .attr('width', width-2)
 .attr('class', 'curtain')
 .attr('transform', 'rotate(180)')
 .style('fill', '#F0F0F0')
        
  curtain.transition()
 .duration(1500)
 //.ease("linear")
 .attr('x', -2 * width)
            
            
        svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 1)
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
       //.style("text-decoration", "underline")  
        .text("Last two weeks: "+data["max_14"]);
    
      svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 15)
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
       //.style("text-decoration", "underline")  
        .text("Total: "+data["max"]);
    
   /* console.log(d3.selectAll(".tick").each(function(d) {
        
        console.log(d3.select(d)._groups);
       
    }));*/
             
    }
    
   
       function turn_off(){
        
        document.getElementById("plot").style.visibility="hidden";
   document.getElementById("features").style.visibility="hidden";
    }
   
//document.getElementById("mySelect").addEventListener("click",change_map);  