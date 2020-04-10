import urllib.request
import json
from time import sleep
from hashlib import md5
import argparse
import sys
import os
import yaml
sys.path.append('../classes')
import notify
from common import Common

if __name__ == "__main__":
    env_path = "../../.env.yml"
    with open(env_path) as file:
        yml = yaml.load(file, Loader=yaml.SafeLoader)

    list_path = "../../docs/data/collection/collection.json"

    count = 0

    with open(list_path) as f:
        df = json.load(f)
        collections = df["collections"]
        for collection in collections:
            collection_name = collection["@id"].split("/")[-1].split(".")[0]
            print(collection_name)

            output_dir = yml["json_dir"] + "/iiif/collections/" + collection_name

            os.makedirs(output_dir, exist_ok=True)

            path = "../../docs/data/collection/collections/"+collection_name+".json"

            if not os.path.exists(path):
                continue

            with open(path) as f:
                df = json.load(f)

                for e in df["manifests"]:

                    manifest = e["@id"]

                    output_path = output_dir + "/" + Common.getId(manifest) + ".json"

                    if not os.path.exists(output_path):

                        if count % 100 == 0:
                            print(str(count) + "\t" + manifest)
                            notify.Notify.send("dwn from collections\t"+str(count), env_path)

                        count += 1

                        sleep(0.5)

                            
                        try:

                            Common.download(manifest, output_path)

                        except Exception as e:
                            print(manifest+"\t"+str(e))
