from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import time
from string import join
import pandas as pd
import cPickle

MONGO = True
JURIS = None
FEASIBILITY = True

cid = "ZC7yyAyA8jkDFnRtf" # parcels
csvname = "output/parcels.csv"

if FEASIBILITY:
    cid = "hMm5FqbDCPa4ube6Y" # feasibility
    csvname = "output/feasibility.csv"

if MONGO:
    client = MongoClient()
    #client.drop_database("baus")
    db = client.togethermap
else:
    outf = open("parcels.json", "w")

df = pd.read_csv(csvname, index_col="geom_id")

cnt = 0
features = []

print time.ctime()


def export_features(features):
    global MONGO, db, outf
    if MONGO:
         db.places.insert_many(features)
    else:
         outf.write(join([json.dumps(f) for f in features], "\n"))

parcels = cPickle.load(open("output/parcels.pickle"))

for geom_id, geojson in parcels:

             cnt += 1
             if cnt % 10000 == 0:
                 print "Done reading rec %d" % cnt

             if len(features) == 10000:

                 print "Exporting 10k recs"
                 export_features(features)
                 print "Done exporting 10k recs"

                 features = []

             try:
                 rec = df.loc[geom_id]
             except:
                 # don't need to keep it, it's not in parcels.csv
                 continue
    
             if JURIS and rec["juris"] != JURIS:
                 continue

             f = json.loads(geojson)

             f["properties"] = rec.to_dict()
             f["properties"]["geom_id"] = geom_id
             del f["id"]

             f["creatorUID"] = "ceTir2NKMN87Gq7wj"
             f["creator"] = "Fletcher Foti"
             f["createDate"] = "2015-08-29T05:10:00.446Z"
             f["updateDate"] = "2015-08-29T05:10:00.446Z"
             f["collectionId"] = cid
             f['_id'] = str(ObjectId())
             f["post_count"] = 0

             features.append(f)
                 
if len(features):
    export_features(features)

print time.ctime()
