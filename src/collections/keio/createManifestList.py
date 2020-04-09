import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import sys
sys.path.append('../../classes')
import notify

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

manifest_arr = []

def scrape_for_page(url):
    flg = True

    print("page\t" + url)

    sleep(1)

    r = requests.get(url,verify=False)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(r.text, "lxml")

    arr_div = soup.find_all(class_="search-result-image")

    if len(arr_div) > 0:
        for div in arr_div:

            href = div.find("a").get("href")

            params = href.split("?")[1].split("&")

            archive = params[0].split("=")[1]
            id = params[1].split("=")[1]

            manifest = "http://dcollections.lib.keio.ac.jp/sites/default/files/iiif/"+archive+"/"+id+"/manifest.json"

            
            manifest_arr.append(manifest)
            print(manifest)

            if len(manifest_arr) % 100 == 1:
                notify.Notify.send("keio\t"+str(len(manifest_arr)), "../../classes/env.yml")

    else:
        flg = False

    return flg

output_path = "data/manifest_list.csv"

base_url = "http://dcollections.lib.keio.ac.jp/ja/collections/search/%2520?page="

loop_flg = True
page = 0

while loop_flg:
    url = base_url + str(page)

    loop_flg = scrape_for_page(url)

    page += 1

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

for manifest in manifest_arr:
    writer.writerow([manifest])

f.close()
