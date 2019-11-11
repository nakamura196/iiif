import urllib.request
from bs4 import BeautifulSoup
import csv
import requests
import os
import json
import time

for i in range(200020011, 990256698):
    url = "https://kotenseki.nijl.ac.jp/biblio/"+str(i)+"/manifest"

    opath = "/Users/nakamura/git/d_iiif/iiif/src/collections/nijl/data/json/"+str(i)+".json"

    if not os.path.exists(opath):

        print(i)

        fw = open(opath, 'w')
        
        headers = {"content-type": "application/json"}

        time.sleep(0.5)

        r = requests.get(url, headers=headers)

        try:
            data = r.json()
            
        except:
            data = {}
            print("err")

        json.dump(data, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        # break

