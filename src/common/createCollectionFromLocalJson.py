import json
import argparse
import sys
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


if __name__ == "__main__":
    args = parse_args()

    collection_name = args.collection_name

    input_dir = "../../json/collections/" + collection_name

    output_path = "../../docs/data/collection/collections/" + collection_name + ".json"

    files = glob.glob(input_dir + "/*.json")

    manifests = []

    for i in range(len(files)):

        file = files[i]

        with open(file, 'r') as f:
            try:
                data = json.load(f)

                if "@type" in data and data["@type"] == "sc:Manifest":

                    manifest = data["@id"]

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

                    canvas = data["sequences"][0]["canvases"][0]
                    resource = canvas["images"][0]["resource"]
                    thumbnail = ""
                    if "service" in resource:
                        thumbnail = resource["service"]["@id"] + \
                                                "/full/200,/0/default.jpg"
                    else:
                        thumbnail = canvas["thumbnail"]["@id"]

                    if thumbnail != "":
                        manifest_obj["thumbnail"] = thumbnail

            except:
                continue

    collection = dict()
    collection["@context"] = "http://iiif.io/api/presentation/2/context.json"
    collection["@id"] = "https://nakamura196.github.io/iiif/data/collection/collections/" + collection_name + ".json"
    collection["@type"] = "sc:Collection"
    collection["vhint"] = "use-thumb"
    collection["manifests"] = manifests

    fw = open(output_path, 'w')
    json.dump(collection, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
