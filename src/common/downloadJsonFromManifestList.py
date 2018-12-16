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


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

if __name__ == "__main__":
    args = parse_args()

    type = args.type

    list_path = "../collections/"+type+"/data/manifest_list.csv"
    output_dir = "../../json/collections/"+type

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
                    with open(output_dir+"/"+make_md5(manifest)+".json", 'w') as outfile:
                        json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

            except urllib.error.URLError as e:
                # with open(path, 'w') as outfile:
                print(e.reason+"\t"+manifest)
