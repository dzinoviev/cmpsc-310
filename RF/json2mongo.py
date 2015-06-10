import glob, json
from pymongo import MongoClient

client = MongoClient()

db = client.RecordedFuture
entities = db.entities
instances = db.instances
entities.remove ()
instances.remove ()

i_keys = {}
e_keys = {}

for f in glob.glob ('2008-KZ-*.json'):
    with open (f) as infile:
        data = json.load (infile)

        i_data = []
        for inst in data["instances"]:
            if inst["id"] not in i_keys:
                inst["_id"] = inst["id"]
                i_data.append (inst)    
                i_keys[inst["id"]] = inst["id"]
        if i_data:
            instances.insert_many (i_data)

        e_data = []
        for key in data["entities"]:
            if key not in e_keys:
                data["entities"][key]["_id"] = key
                e_data.append ( data["entities"][key])
                e_keys[key] = key
        if e_data:
            entities.insert_many (e_data)

print ("Entities:", entities.count ())
print ("Instances:", instances.count ())
