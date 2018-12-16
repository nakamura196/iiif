import urllib.request
import os
import csv
import json
from time import sleep
from hashlib import md5
import argparse
import sys

def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'type',
        action='store',
        type=str,
        help='type')

    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_args()

    type = args.type

    list_path = "../collections/"+type+"/data/manifest_list.csv"
    output_path = "../../docs/data/collection/collections/"+type+".json"

    manifests = []

    with open(list_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばしたい時

        count = 0

        for row in reader:
            manifest = row[0]

            if count % 20 == 0:

                print(str(count)+"\t"+manifest)

            count += 1

            try:

                sleep(1)

                r = urllib.request.urlopen(manifest)

                # json_loads() でPythonオブジェクトに変換
                data = json.loads(r.read().decode('utf-8'))

                if "@type" in data and data["@type"] == "sc:Manifest":
                    label = ""
                    if "label" in data:
                        label = data["label"]

                    manifest_obj = dict()
                    manifests.append(manifest_obj)
                    manifest_obj["@id"] = manifest
                    manifest_obj["@type"] = "sc:Manifest"
                    manifest_obj["label"] = label
                    if "license" in data:
                        manifest_obj["license"] = data["license"]

            except urllib.error.URLError as e:
                # with open(path, 'w') as outfile:
                print(e.reason+"\t"+manifest)

    collection = dict()
    collection["@context"] = "http://iiif.io/api/presentation/2/context.json"
    collection["@id"] = "https://nakamura196.github.io/iiif/data/collection/collections/" + type + ".json"
    collection["@type"] = "sc:Collection"
    collection["manifests"] = manifests

    fw = open(output_path, 'w')
    json.dump(collection, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
