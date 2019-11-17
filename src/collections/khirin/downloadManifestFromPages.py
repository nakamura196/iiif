import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import glob
import pandas as pd
from time import sleep
from hashlib import md5
import argparse
import sys
import os
import requests
import json

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


output_dir = "../../../json/collections/khirin"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

files = glob.glob("data/pages/*.csv")
for i in range(len(files)):
    file = sorted(files)[i]

    print(file)

    filename = file.split("/")[-1]

    csv_path = "data/done/"+filename
    if os.path.exists(csv_path):
        continue

    df = pd.read_csv(file)

    r_count = len(df.index)
    c_count = len(df.columns)

    for r in range(1, r_count):
        row = []
        for c in range(0, c_count):
            value = df.iloc[r, c]
            # print(value)
            row.append(value)
        
        url = row[0]
        print(url)

        html = urllib.request.urlopen(url)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")

        arr_a = soup.find_all("div")

        # print(arr_a)

        for a in arr_a:
            href = a.get("data-object")
            # print(href)
            if href != None and "mirador" in href:
                # print(href)
                manifest = href.split("=")[1].split("&")[0]
                print(manifest)

                output_path = output_dir + "/" + make_md5(manifest) + ".json"

                if not os.path.exists(output_path):

                    try:

                        # sleep(0.5)

                        headers = {"content-type": "application/json"}
                        r = requests.get(manifest, headers=headers, verify=False)
                        data = r.json()

                        # print(data)

                        with open(output_path, 'w') as outfile:
                            json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True,
                                        separators=(',', ': '))

                    except Exception as e:
                        print(manifest)
                        print(e)
                        print("----")

    with open(csv_path, 'w') as outfile:
        json.dump({}, outfile, ensure_ascii=False, indent=4, sort_keys=True,
                    separators=(',', ': '))
