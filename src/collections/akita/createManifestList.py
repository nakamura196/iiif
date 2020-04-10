import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep

manifest_arr = []

def handle_expands(base_url):

    r = requests.get(url,verify=False)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(r.text, "lxml")

    expand_arr = soup.find_all(class_="expand")

    for expand in expand_arr:
        href = expand.find("a").get("href")
        id = href.split("/item/")[1]
        manifest = "https://da.apl.pref.akita.jp/lib/iiif/"+id+"/manifest.json"
        manifest_arr.append(manifest)

loop_flg = True
page = 1

output_path = "data/manifest_list.csv"

while loop_flg:

    url = "https://da.apl.pref.akita.jp/lib/search?period=0&c=lib&c=bungaku&c=moma&c=mus&c=koubun&c=maibun&c=lifelong&radio-facility=lib&kw=&title=&mode=advance&mode=advance&q=&ct=lib&sourceType=0&person=&from=&to=&vt=&page=" + str(page)

    print("page\t" + url)

    sleep(1)

    r = requests.get(url,verify=False)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(r.text, "lxml")

    arr_h3 = soup.find_all(class_="result-title")

    if len(arr_h3) > 0:
        for h3 in arr_h3:
            href = "https://da.apl.pref.akita.jp/" + h3.find("a").get("href")
            id = href.split("/item/")[1]
            manifest = "https://da.apl.pref.akita.jp/lib/iiif/"+id+"/manifest.json"
            manifest_arr.append(manifest)
            
            # expandがあれば
            handle_expands(href)

    else:
        loop_flg = False

    page += 1

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

for manifest in manifest_arr:
    writer.writerow([manifest])

f.close()
