import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

manifest_arr = []

url = "https://raw.githubusercontent.com/nakamura196/portal_pro/master/docs/data/collection.json"

collections = requests.get(url).json()

collections = collections["collections"]

for collection in collections:
    print(collection["label"])
    collection = requests.get(collection["@id"]).json()

    manfiests = collection["manifests"]

    for manifest in manfiests:
        manifest_arr.append(manifest["@id"])

f = open("data/manifest_list.csv", 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

for manifest in manifest_arr:
    writer.writerow([manifest])

f.close()
