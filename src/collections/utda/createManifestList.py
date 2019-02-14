import csv
import glob
import json

if __name__ == '__main__':

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    dir = "/Users/nakamura/git/dataset/docs/collections/*/image/collection.json"
    files = glob.glob(dir)

    for file in files:
        f = open(file, 'r')
        json_dict = json.load(f)

        manifests = json_dict["manifests"]

        for manifest in manifests:
            manifest_arr.append(manifest["@id"])

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    f.close()
