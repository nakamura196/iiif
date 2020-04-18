import sys
sys.path.append('../classes')
from common import Common
import json
import argparse
import os
import glob
import yaml
import pandas as pd


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'collection_name',
        action='store',
        type=str,
        help='collection_name')

    return parser.parse_args(args)


env_path = "../../.env.yml"
with open(env_path) as file:
    yml = yaml.load(file, Loader=yaml.SafeLoader)

args = parse_args()

collection_name = args.collection_name

input_dir = yml["json_dir"] + "/iiif/collections/" + collection_name

output_path = "../../docs/data/collection/collections/" + collection_name + ".json"

list_path = "../collections/" + collection_name + "/data/manifest_list.csv"

manifests = []

license_check = {}

df = pd.read_csv(list_path)

for i in range(len(df.index)):

    if i % 100 == 0:
        print(str(i+1)+"\t"+str(len(df.index)))

    manifest = df.iloc[i, 0]

    uuid = Common.getId(manifest)

    file = input_dir + "/" + uuid + ".json"

    if not os.path.exists(file):
        print("Not e\t"+file)
        continue
        
    with open(file, 'r') as f:
        try:
            data = json.load(f)

            if "@type" in data and data["@type"] == "sc:Manifest":

                # 画像がない場合はスキップ

                ##################

                if "thumbnail" not in data:

                    thumbnail = Common.getThubmnail(data)

                    if thumbnail != None:
                        data["thumbnail"] = thumbnail

                ##################

                license = ""

                if "license" in data:
                    license = data["license"].strip()

                ##################

                label = ""
                if "label" in data:
                    if "@value" in data["label"][0]:
                        label = data["label"][0]["@value"]
                    else:
                        label = data["label"]

                ##################

                # manifest = data["@id"]

                manifest_obj = dict()

                manifest_obj["@id"] = manifest
                manifest_obj["@type"] = "sc:Manifest"
                manifest_obj["label"] = label

                if license != "":
                    manifest_obj["license"] = license

                manifest_obj["thumbnail"] = data["thumbnail"]

                manifests.append(manifest_obj)

                ##################

                if license not in license_check:
                    print("----------------")
                    print("'"+license+"'\t"+data["@id"])
                    license_check[license] = 0

                license_check[license] += 1

        except Exception as e:
            print(e)
            continue

collection = dict()
collection["@context"] = "http://iiif.io/api/presentation/2/context.json"
collection["@id"] = "https://nakamura196.github.io/iiif/data/collection/collections/" + \
    collection_name + ".json"
collection["@type"] = "sc:Collection"
collection["vhint"] = "use-thumb"
collection["manifests"] = manifests

fw = open(output_path, 'w')
json.dump(collection, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))

for license in license_check:
    print(license+"\t"+str(license_check[license]))

print("manifest size:\t"+str(len(manifests)))
