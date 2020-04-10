import urllib.request
import csv
import json
from time import sleep
from hashlib import md5
import argparse
import sys
import os
import requests
sys.path.append('../classes')
import notify
import yaml

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


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


if __name__ == "__main__":
    args = parse_args()

    env_path = "../../.env.yml"
    with open(env_path) as file:
        yml = yaml.load(file)

    collection_name = args.collection_name

    list_path = "../collections/" + collection_name + "/data/manifest_list.csv"
    output_dir = yml["json_dir"]+"/iiif/collections/" + collection_name

    os.makedirs(output_dir, exist_ok=True)

    manifests = []

    with open(list_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばしたい時

        count = 0

        for row in reader:

            manifest = row[0]

            if count % 20 == 0:
                print(str(count) + "\t" + manifest)

            if count % 500 == 0:
                notify.Notify.send("dwn\t"+collection_name+"\t"+str(count), env_path)

            count += 1

            output_path = output_dir + "/" + make_md5(manifest) + ".json"

            if not os.path.exists(output_path):

                try:

                    sleep(0.5)

                    r = requests.get(manifest, verify=False)
                    data = r.json()

                    # print(data)

                    with open(output_path, 'w') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True,
                                    separators=(',', ': '))

                except Exception as e:
                    print(manifest)
                    print(e)
                    print("----")
