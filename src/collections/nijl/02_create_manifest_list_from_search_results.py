import urllib.request
from bs4 import BeautifulSoup
import csv
import requests
import os
import json
import time
import glob

manifest_arr = []

output_path = "data/manifest_list.csv"

files = glob.glob("data/result/*.json")

check = {}

for i in range(len(sorted(files))):

    file = files[i]


    with open(file) as f:
        try:
            df = json.load(f)
        except:
            continue

        for obj in df:
            
            id = obj["_id"]
            # print(id)
            manifest = "https://kotenseki.nijl.ac.jp/biblio/"+str(id)+"/manifest"
        

            if manifest not in manifest_arr:
                manifest_arr.append(manifest)
            else:
                if id not in check:
                    check[id] = []
                check[id].append(file)

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

for manifest in manifest_arr:
    writer.writerow([manifest])

f.close()



print(len(manifest_arr))

for id in check:
    print(id)
    print(check[id])
    print("---")