# US Counties — EndCoronavirus.org

US COUNTY-LEVEL MAPS and classification of COVID-19 cases

Created by: Olha Buchel from the New England Complex Systems Institute 
  and Joseph D. Ortiz from Kent State University, Department of Geology. 

Code to generate the interactive maps at  <https://www.endcoronavirus.org/us-counties>

## Installation

You can install dependencies (e.g. pandas, ansible, boto3)  for this project by using [pipenv](https://pipenv.pypa.io/en/latest/).

    $ pipenv install
    $ pipenv shell
    
This creates a local environment with all necessary packages installed.

## Web site setup and data flow

The page <https://www.endcoronavirus.org/us-counties> is hosted by SquareSpace.
It embeds <https://obuchel.github.io/classification/classification_map.html> in an IFrame.

### classification/classification_ids_counties2.json

Contains the county-by-county classification with records like 
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

### Reading: CSSEGISandData
 
https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv


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
with one entry per county.
This file is apparently included in the github repository
as classification/classification_ids_counties2.json.

## Development

### Testing locally

Run a local web server

    $ python -m http.server

Then open http://localhost:8000.
This will serve JSON files directly from the local directories `output` and `data/geo`.


# Workflow for updating the maps

We want to keep the county-level JSON files out of the GitHub repository,
therefore we serve them from an S3 bucket.


## Setup: Get your credentials for AWS S3

Make sure you have AWS credentials (Access key ID, Secret access key) for API access.
Now we need to make the credentials accessible to the ansible playbooks (see below).

### Option 1: Using the AWS command line interface

Install from https://aws.amazon.com/cli/

Then run 

    $ aws configure
    
This will prompt you for your AWS Access Key ID etc.

**Note:** Never commit credentials to git.

### Option 2: Using direnv

You can use the [direnv](https://direnv.net/) tool and create a `.envrc` file in your home directory

**Note:** Never commit credentials to git.

## Setup: Prepare the S3 bucket

You only need to do this once:

    $ ansible-playbook playbooks/setup_s3_bucket.yml
     
This will create an S3 bucket (if necessary) and set its permissions to public readable. It also sets up a CORS configuration that allows access to the JSON files from browsers.

The name of the bucket is configured in `playbooks/settings.yml`.

## Daily update

To update the maps at https://www.endcoronavirus.org/us-counties:

1. Check out the code locally
2. Run `prepare_classification_counties_final.py`. The script will
   - retrieve current data as a csv file
   - do the analysis
   - write one JSON file per county into `output/classification`
3. Upload the generated files from `output/classification`  and `data/geo` to S3 with

       $ ansible-playbook playbooks/upload_to_s3.yml
       
   Unfortunately, this may take a while, depending on your internet connection.
   (I have seen a runtime of 27 minutes on a slow internet connection)
