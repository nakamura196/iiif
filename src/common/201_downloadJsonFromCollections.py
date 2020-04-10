import urllib.request
import json
from time import sleep
from hashlib import md5
import argparse
import sys
import os
import yaml

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


if __name__ == "__main__":
    env_path = "../../.env.yml"
    with open(env_path) as file:
        yml = yaml.load(file)

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

            with open("../../docs/data/collection/collections/"+collection_name+".json") as f:
                df = json.load(f)

                for e in df["manifests"]:

                    manifest = e["@id"]

                    output_path = output_dir + "/" + make_md5(manifest) + ".json"

                    if not os.path.exists(output_path):

                        if count % 100 == 0:
                            print(str(count) + "\t" + manifest)

                        count += 1

                        try:

                            sleep(1)

                            r = urllib.request.urlopen(manifest)

                            # json_loads() でPythonオブジェクトに変換
                            try:
                                data = json.loads(r.read().decode('utf_8'))

                                with open(output_path, 'w') as outfile:
                                    json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True,
                                            separators=(',', ': '))

                            except Exception as e:
                                print(manifest+"\t"+str(e))

                        except urllib.error.URLError as e:
                            print(e.reason + "\t" + manifest)
