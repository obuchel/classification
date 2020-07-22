import json
import fiona
from shapely.geometry import mapping, LineString, MultiLineString
 
file = '/Users/olgabuchel/Downloads/ISR_adm/untitled folder/ISR_adm1.shp'
with fiona.open(file, 'r') as ds_in:
    num_tiles = 10
    schema = {
    "geometry": "MultiLineString",
    "properties": {"id": "int"}
     }
print(ds_in.bounds)
#'IL': ('Israel', (34.2654333839, 29.5013261988, 35.8363969256, 33.2774264593)),
minx, miny, maxx, maxy = [34.2654333839,29.5013261988, 35.8363969256, 1.5709635417*1+29.5013261988]#31.7064629176]#33.2774264593]
dx = (maxx - minx) / num_tiles
dy = (maxy - miny) / num_tiles
print(range(num_tiles + 1))
lines = {}
lines["type"]="FeatureCollection"
lines["features"]=[]

for x in range(num_tiles + 1):
    for y in range(num_tiles + 1):
        #print((minx + x * dx, miny), (minx, miny + y * dy),(minx + x * dx, maxy),(maxx, miny + y * dy))
        aa=(minx + x * dx, miny)
        bb=(minx, miny + y * dy)
        cc=(minx + x * dx, maxy)
        dd=(maxx, miny + y * dy)
        print(minx + x * dx,miny + y * dy)
        lines["features"].append({"type":"Feature","geometry":{"type":"Point","coordinates":[minx + x * dx+dx/2,miny + y * dy+dy/2]},"properties":{"name":"feature"}})


minx, miny, maxx, maxy = [34.2654333839,29.5013261988+1.5709635417, 35.8363969256, 1.5709635417*2+29.5013261988]#31.7064629176]#33.2774264593]                                         
dx = (maxx - minx) / num_tiles
dy = (maxy - miny) / num_tiles

for x in range(num_tiles + 1):
    for y in range(num_tiles + 1):
        #print((minx + x * dx, miny), (minx, miny + y * dy),(minx + x * dx, maxy),(maxx, miny + y * dy))                                                                 
        aa=(minx + x * dx, miny)
        bb=(minx, miny + y * dy)
        cc=(minx + x * dx, maxy)
        dd=(maxx, miny + y * dy)
        print(minx + x * dx,miny + y * dy)
        lines["features"].append({"type":"Feature","geometry":{"type":"Point","coordinates":[minx + x * dx+dx/2,miny + y * dy+dy/2]},"properties":{"name":"feature"}})

        
with open("grid_israel.json","w") as ds_dst:
    json.dump(lines,ds_dst)
'''
driver=ds_in.driver,
{'AeronavFAA': 'r', 'ARCGEN': 'r', 'BNA': 'raw', 'DXF': 'raw', 'CSV': 'raw', 'OpenFileGDB': 'r', 'ESRIJSON': 'r', 'ESRI Shapefile': 'raw', 'GeoJSON': 'rw', 'GPKG': 'rw', 'GML': 'raw', 'GPX': 'raw', 'GPSTrackMaker': 'raw', 'Idrisi': 'r', 'MapInfo File': 'raw', 'DGN': 'raw', 'S57': 'r', 'SEGY': 'r', 'SUA': 'r', 'TopoJSON': 'r'}
'''
