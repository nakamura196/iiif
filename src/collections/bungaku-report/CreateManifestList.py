import csv
from time import sleep
import requests
import json

output_path = "data/manifest_list.csv"

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

base_url = "https://omeka.bungaku-report.com/iiif/collection/1%2C"

sleep(1)

r = requests.get(base_url)
data = r.json()

manifests = data["manifests"]

for manifest in manifests:
    writer.writerow([manifest["@id"]])

f.close()
