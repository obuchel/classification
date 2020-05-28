# US Counties — EndCoronavirus.org

US COUNTY-LEVEL MAPS and classification of COVID-19 cases

Created by: Olha Buchel from the New England Complex Systems Institute 
  and Joseph D. Ortiz from Kent State University, Department of Geology. 

Code to generate the interactive maps at  <https://www.endcoronavirus.org/us-counties>

## Web site setup and data flow

The page <https://www.endcoronavirus.org/us-counties> is hosted by SquareSpace.
It embeds <https://obuchel.github.io/classification/classification_map.html> in an IFrame.

In the source code of that HTML page you find several data sources

```js
fetch('classification/classification_ids_counties2.json')

fetch('counties.json')
 
 if (["630","16","316","580","850"].indexOf(num)>-1) {
    
    var url='classification/data_counties_'+num+'.json';
} else {
    
    var url='classification/data_counties_840'+num+'.json';
}
fetch(url)
```

### classification/classification_ids_counties2.json

Has records like 
```json
{
    "n": "Cuming, Nebraska, US",
    "id": 84031039,
    "v": 0.8484848484848485,
    "c": "red",
    "max": 22
}
``` 

### counties.json

This is a shapefile (JSON format), with records like
```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
       "lots of lon-lat pairs."
    ]
  },
  "properties": {
    "STATEFP": "31",
    "COUNTYFP": "039",
    "COUNTYNS": "00835841",
    "GEOID": "31039",
    "NAME": "Cuming",
    "NAMELSAD": "Cuming County",
    "LSAD": "06",
    "CLASSFP": "H1",
    "MTFCC": "G4020",
    "CSAFP": "",
    "CBSAFP": "",
    "METDIVFP": "",
    "FUNCSTAT": "A",
    "ALAND": 1477895811,
    "AWATER": 10447360,
    "INTPTLAT": "+41.9158651",
    "INTPTLON": "-096.7885168",
    "value": 2
  }
}
```

From [here](http://oksovi.geog.okstate.edu/_downloads/91156eb3f0f4b16f07e08bf65dc10ca6/Part%203-%20Geopandas.html) we can figure out some relevant fields:

- `"GEOID": "31039"`, this matches the `"id": 84031039` shown in `classification_ids_counties2.json` above.
- STATEFP is the State FIP code
- value: not sure yet where that comes from, and what it is used for

### 'classification/data_counties_'+num+'.json'

Data for a given county, indexed by its GEOID, prepended with '840' (except for a handful of counties.)
These are time series for the county, here are the most recent 4 values for Cuming County:

```json
{
  "dates": ["5/19/20", "5/20/20", "5/21/20", "5/22/20"],
  "max_14": 22,
  "max": 32,
  "value": [1.55, 1.5, 1.45, 1.4 ],
  "time": [ "5/24/20", "5/25/20", "5/26/20", "5/27/20" ],
  "original_values": [0, 0, 0, 0]
}
```

My interpretation for the fields:

- dates is the x axis for the time series
- max_14 maximum case count last 14 days
- max maximum case count
- value smoothed case count
- time looks redundant
- original_values the case counts

## Data flow on the python side

The script `prepare_classification_counties_final.py` is used to write the JSON files for the website.
Just like with the JavaScript on the web page, you can look for `open()` in the python file.

### my_ids.json

This looks unused.

### Reading CSSEGISandData
 
https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')


### Writing: 'data_counties_'+str(ids[recs.index(name)]["UID"])+'.json'

These are the files with the county data.

### Writing: data_counties.json

This is a list of records like this:

```python
{
    "color":color,
    "province":name.split(",")[0],
    "country":name.split(",")[1],
    "id":"new_id_"+str(ind4),
    "value1":ratio, 
    "dates":tim2,
    "value":y3
}
```
presumably one entry per county.
This file is apparently included in the github repository
as classification/data_counties.json.

### Writing: classification_ids_counties2.json

This is a list of records like this:

```python
{
    "n": name, 
    "id": ids[recs.index(name)]["UID"], 
    "v": ratio, 
    "c": color,
    "max": int(max(y5))
}
```
presumably one entry per county.
This file is apparently included in the github repository
as classification/classification_ids_counties2.json.

