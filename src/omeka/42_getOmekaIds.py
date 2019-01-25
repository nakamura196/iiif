import urllib.request
import json, rdflib_jsonld
import csv
import sys
import argparse


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


if __name__ == "__main__":
    args = parse_args()

    collection_name = args.collection_name

    path = "data"

    output_path = path + "/"+collection_name+"/oids.csv"

    fo = open(output_path, 'w')
    writer = csv.writer(fo, lineterminator='\n')
    writer.writerow(
        ["identifier", "id", "manifest"])

    flg = True
    page = 1

    while flg:
        url = "http://iiif2.dl.itc.u-tokyo.ac.jp/api/items?item_set_id=" + args.item_set_id + "&page=" + str(page)
        print(url)

        page += 1

        response = urllib.request.urlopen(url)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body)

        if len(data) > 0:
            for i in range(len(data)):
                obj = data[i]

                ident = obj["dcterms:identifier"][0]["@value"]
                id = obj["o:id"]
                manifest = ""
                if "dcterms:references" in obj:
                    manifest = obj["dcterms:references"][0]["@id"]

                writer.writerow([ident, id, manifest])

        else:
            flg = False

    fo.close()
