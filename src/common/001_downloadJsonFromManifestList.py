import requests
import os
import argparse
from time import sleep
import json
import csv
import urllib.request

import yaml
import sys
sys.path.append('../classes')

from notify import Notify
from common import Common


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
                Notify.send("dwn\t"+collection_name+"\t"+str(count), env_path)

            count += 1

            output_path = output_dir + "/" + Common.getId(manifest) + ".json"

            if not os.path.exists(output_path):

                sleep(0.5)

                try:

                    Common.download(manifest, output_path)

                except Exception as e:
                    print(manifest)
                    print(e)
                    print("----")
