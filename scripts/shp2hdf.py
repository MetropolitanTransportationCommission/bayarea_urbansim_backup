import fiona
from shapely.geometry import shape
import pandas as pd
import json
import time
from string import join
import cPickle

print time.ctime()

def add_bbox(p):
    bounds = shape(p['geometry']).bounds
    minx, miny, maxx, maxy = bounds
    poly = {
        "type": "Polygon",
        "coordinates": [
            [ [minx, miny], [minx, maxy], [maxx, maxy],
              [maxx, miny], [minx, miny] ]
        ]
    }
    p['bbox'] = poly
    return p

store = pd.HDFStore("parcels.h5", "w")

features = []

with fiona.drivers():
    with fiona.open('/home/ubuntu/data/parcels4326.shp') as shp:
        
        for f in shp:

             if f["geometry"] is None:
                 continue

             geom_id = int(f["properties"]["GEOM_ID"])
    
             f["properties"] = {}

             f = add_bbox(f)

             features.append((geom_id, json.dumps(f)))

             if len(features) % 5000 == 0: print len(features)

cPickle.dump(features, open("parcels.pickle", "w"))

#geomids, geojson = zip(*features)
#s = pd.Series(geojson, index=geomids)
#store["parcels"] = pd.DataFrame({"geojson": s})
#store.close()

print time.ctime()
