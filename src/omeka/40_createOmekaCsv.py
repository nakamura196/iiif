import json, rdflib_jsonld
import csv
from hashlib import md5
import sys
import argparse
import glob
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

    path = "../../json/collections/" + collection_name
    data_path = path
    files = glob.glob(path + "/*.json")

    fields = []
    fields.append("dcterms:identifier")
    fields.append("Media Url")
    fields.append("dcterms:title")
    fields.append("resource template")
    fields.append("Collection Identifier")
    fields.append("Resource Type")

    result = []

    obj = dict()
    obj["dcterms:identifier"] = collection_name
    obj["dcterms:title"] = collection_name
    obj["resource template"] = "Item-set"
    obj["Resource Type"] = "Item Set"
    result.append(obj)

    for i in range(len(files)):

        file = files[i]

        if i % 100 == 0:
            print(str(i + 1) + "/" + str(len(files)))

        with open(file, 'r') as f:
            try:
                array = json.load(f)
            except:
                continue

        obj = dict()

        obj["dcterms:identifier"] = make_md5(array["@id"], encoding='utf-8')

        try:
            canvas = array["sequences"][0]["canvases"][0]
            resource = canvas["images"][0]["resource"];
            if "service" in resource:
                obj["Media Url"] = resource["service"]["@id"] + "/full/600,/0/default.jpg"
            else:
                obj["Media Url"] = canvas["thumbnail"]["@id"]

        except:
            print("Error.\t" + array["@id"])

        obj["resource template"] = "item"
        obj["Collection Identifier"] = collection_name
        obj["Resource Type"] = "Item"

        result.append(obj)

    dir = 'data/' + collection_name
    os.makedirs(dir, exist_ok=True)

    with open(dir + '/omeka_csv_import.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく

        writer.writerow(fields)

        for obj in result:
            list = []
            for field in fields:
                value = ""
                if field in obj:
                    value = obj[field]

                list.append(value)
            writer.writerow(list)
