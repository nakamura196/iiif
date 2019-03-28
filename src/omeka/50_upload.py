import csv
import sys
import argparse
import json
import requests
import datetime
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

    parser.add_argument(
        'item_set_id',
        action='store',
        type=str,
        help='item_set_id')

    return parser.parse_args(args)


def get_properties():
    with open("data/properties.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばしたい時

        properties = {}

        for row in reader:
            properties[row[0]] = row[1]

        return properties


def get_ids():
    with open("data/ids.csv", 'r') as f:
        reader = csv.reader(f)
        # header = next(reader)  # ヘッダーを読み飛ばしたい時

        ids = []

        for row in reader:
            ids.append(row[6])

        return ids


def add_param(type, pid, value):
    obj = {}
    obj["property_id"] = int(pid)
    if type == "literal":
        obj["type"] = type

        obj["@value"] = value
    else:
        obj["type"] = type

        obj["@id"] = value

    return obj


if __name__ == "__main__":
    args = parse_args()

    collection_name = args.collection_name

    csv_path = "data/" + collection_name + "/metadata.csv"

    properties = get_properties()
    ids = get_ids()
    column_map = {}

    endpoint = "http://iiif2.dl.itc.u-tokyo.ac.jp/api"

    f = open("data/config.yml", "r+")
    config = yaml.load(f)

    key_identity = config["key_identity"]
    key_credential = config["key_credential"]

    temp_id = 10
    item_set_id = args.item_set_id

    items_url = endpoint + "/items?search="

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)

        row_count = 0

        for row in reader:

            param = {}

            if row_count == 0:

                for i in range(0, len(row)):
                    term = row[i]
                    if term in properties:
                        column_map[i] = term

            else:

                id = row[0]

                if id in ids:
                    continue

                if row_count % 100 == 1:
                    print(row_count)
                    print(datetime.datetime.now())

                # 読み込むオブジェクトの作成
                # r = requests.get(url=items_url + id)
                # if len(r.json()) > 0:
                #     continue

                for column_count in column_map:
                    term = column_map[column_count]
                    pid = properties[term]
                    value = row[column_count]

                    param[term] = []

                    if value == "":
                        continue

                    if term == "dcterms:isPartOf" or term == "dcterms:rights" or term == "dcterms:relation" or term == "dcterms:references" or term == "dcterms:source" or term == "foaf:thumbnail" or term == "rdfs:seeAlso":
                        param[term].append(add_param("uri", pid, value))

                    else:

                        if term == "dcterms:description":

                            values = value.split("\n")
                            for v in values:
                                param[term].append(add_param("literal", pid, v))

                        elif term == "bibo:abstract":

                            values = value.split(",")

                            for v in values:
                                param[term].append(add_param("literal", pid, v))


                        else:
                            param[term].append(add_param("literal", pid, value))

                temp = {}
                temp["o:id"] = temp_id
                temp["@id"] = endpoint + "/resource_templates/" + str(temp_id)
                param["o:resource_template"] = temp

                item_set = [{
                    "@id": endpoint + "/item_sets/" + str(item_set_id),
                    "o:id": item_set_id
                }]
                param["o:item_set"] = item_set

                url = endpoint + '/items?key_identity=' + key_identity + '&key_credential=' + key_credential
                payload = param

                headers = {'content-type': 'application/json; charset=UTF-8'}

                try:
                    r = requests.post(url, data=json.dumps(payload), headers=headers)
                except:
                    print("Error.")

            row_count += 1
