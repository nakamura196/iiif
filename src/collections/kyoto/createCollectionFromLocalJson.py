import json
import argparse
import sys
import glob
import time

collection_name = "kyoto"

input_dir = "../../../json/collections/" + collection_name

output_path = "../../../docs/data/collection/collections/" + collection_name + ".json"

files = glob.glob(input_dir + "/*.json")

manifests = []

for i in range(len(files)):
    
    if i % 100 == 0:
        print(str(i+1)+"/"+str(len(files)))

    file = files[i]

    with open(file, 'r') as f:

        data = json.load(f)

        if "@type" in data and data["@type"] == "sc:Manifest":

            manifest = data["@id"]

            label = ""
            if "label" in data:
                label = data["label"]

            manifest_obj = dict()
            
            manifest_obj["@id"] = manifest
            manifest_obj["@type"] = "sc:Manifest"
            manifest_obj["label"] = label
            

            canvas = data["sequences"][0]["canvases"][0]
            resource = canvas["images"][0]["resource"]
            thumbnail = ""
            if "service" in resource:
                thumbnail = resource["service"]["@id"] + \
                                        "/full/200,/0/default.jpg"
            else:
                thumbnail = canvas["thumbnail"]["@id"]

            if thumbnail != "":
                manifest_obj["thumbnail"] = thumbnail

            flg = False

            metadata = data["metadata"]
            for obj in metadata:
                if obj["label"] == "権利関係":
                    license = obj["value"]
                    
                    if "画像二次利用自由（所蔵表示）" in license:
                        flg = True
                        manifest_obj["license"] = license.strip()

            if flg:
                manifests.append(manifest_obj)
        

collection = dict()
collection["@context"] = "http://iiif.io/api/presentation/2/context.json"
collection["@id"] = "https://nakamura196.github.io/iiif/data/collection/collections/" + collection_name + ".json"
collection["@type"] = "sc:Collection"
collection["vhint"] = "use-thumb"
collection["manifests"] = manifests

fw = open(output_path, 'w')
json.dump(collection, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))