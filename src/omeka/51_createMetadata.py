from bs4 import BeautifulSoup
import json
import csv
from hashlib import md5
import os
import sys
import unicodedata
import argparse
import glob


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


def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name \
                or "HIRAGANA" in name \
                or "KATAKANA" in name:
            return True
    return False


def format_value(value):
    if isinstance(value, list):

        if len(value) > 0:
            tmp = value[0]
            if "@value" in tmp:
                value = tmp["@value"]
            elif "@id" in tmp:
                return tmp["@id"]
            else:
                value = value[0]
        else:
            return ""
    elif isinstance(value, dict):
        return value["@id"]
    value = str(value)
    value = value.replace('\n', '').replace('\r', '')

    return value


if __name__ == "__main__":
    args = parse_args()

    collection_name = args.collection_name

    path = "../../json/collections/" + collection_name
    data_path = path
    files = glob.glob(path + "/*.json")

    fields = []
    fields.append("dcterms:identifier")
    fields.append("dcterms:title")
    fields.append("dcterms:rights")
    fields.append("dcterms:isPartOf")
    fields.append("dcterms:relation")
    fields.append("rdfs:seeAlso")
    fields.append("dcterms:references")
    fields.append("dcterms:license")
    fields.append("dcterms:description")
    fields.append("sc:attributionLabel")
    fields.append("uterms:databaseLabel")
    fields.append("dcndl:digitizedPublisher")
    fields.append("foaf:thumbnail")
    fields.append("bibo:abstract")
    fields.append("dcterms:source")

    result = []

    fieldsMap = dict()

    import yaml

    f = open("data/" + collection_name + "/config.yml", "r+")
    config = yaml.load(f)

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

        title = "タイトルなし"
        if "label" in array:
            title = array["label"]

        obj["dcterms:title"] = format_value(title)

        description = ""

        if "description" in array:
            description += "Description: " + format_value(array["description"]) + "\n"

        if "related" in array:
            obj["dcterms:relation"] = format_value(array["related"])

        if "seeAlso" in array:
            obj["rdfs:seeAlso"] = array["seeAlso"]

        if "within" in array:
            obj["dcterms:isPartOf"] = array["within"]

        if "viewingHint" in array:
            obj["sc:viewingHint"] = array["viewingHint"]

        if "viewingDirection" in array:
            obj["sc:viewingDirection"] = array["viewingDirection"]

        if "license" in array:
            obj["dcterms:rights"] = array["license"]

        if "license" in array:
            obj["dcterms:license"] = array["license"]

        if "attribution" in array:
            obj["sc:attributionLabel"] = ''.join(
                BeautifulSoup(format_value(array["attribution"]), 'html.parser').findAll(text=True))

        if "logo" in array:
            obj["foaf:thumbnail"] = array["logo"]

        obj["dcterms:references"] = array["@id"]

        labels = []

        canvases = array["sequences"][0]["canvases"]
        for canvas in canvases:
            if "label" in canvas:
                label = canvas["label"]
                if "@value" in label:
                    labels.append(label["@value"])
                elif not label.isnumeric() and not label.replace("[", "").replace("]", "").isnumeric():
                    labels.append(label)

        if len(labels) > 0:
            obj["bibo:abstract"] = ', '.join(labels)

        if "metadata" in array:

            for metadata in array["metadata"]:

                if "value" not in metadata:
                    continue

                label = metadata["label"]
                value = metadata["value"]

                description += label + ": " + value + "\n"

        obj["dcterms:description"] = description

        try:
            canvas = array["sequences"][0]["canvases"][0]
            resource = canvas["images"][0]["resource"]
            if "service" in resource:
                obj["dcterms:source"] = resource["service"]["@id"] + \
                                        "/full/200,/0/default.jpg"
            else:
                obj["dcterms:source"] = canvas["thumbnail"]["@id"]

        except:
            print("Error.\t" + array["@id"])

        # 上書き
        for key in config:
            obj[key] = config[key]

        result.append(obj)

    output_dir = 'data/' + collection_name

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_dir + '/metadata.csv', 'w') as fm:
        writer = csv.writer(fm, lineterminator='\n')  # 改行コード（\n）を指定しておく

        print(fields)
        writer.writerow(fields)

        for obj in result:
            list = []
            for field in fields:
                value = ""
                if field in obj:
                    value = obj[field]

                list.append(value)
            writer.writerow(list)
