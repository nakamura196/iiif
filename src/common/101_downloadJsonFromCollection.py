import urllib.request
import json
from time import sleep
from hashlib import md5
import argparse
import sys
import os


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

    collection_name = args.collection_name

    list_path = "../../docs/data/collection/collections/" + collection_name + ".json"
    output_dir = "/Users/nakamura/git/json/iiif/collections/" + collection_name

    os.makedirs(output_dir, exist_ok=True)

    manifests = []

    with open(list_path) as f:
        df = json.load(f)

    count = 0

    for e in df["manifests"]:

        manifest = e["@id"]

        if count % 20 == 0:
            print(str(count) + "\t" + manifest)

        count += 1

        output_path = output_dir + "/" + make_md5(manifest) + ".json"

        if not os.path.exists(output_path):

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
