import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep

manifest_arr = []


def ff(url):

    r = requests.get(url, verify=False)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(r.text, "lxml")

    arr_e = soup.find_all("a")

    for e in arr_e:
        href = e.get("href")
        if "/manifest" in href:
            manifest = href
            if manifest not in manifest_arr:
                manifest_arr.append(manifest)


output_path = "data/manifest_list.csv"

places = [
    "野津家", "島根大学", "隠岐の島町教育委員会蔵"
]

for place in places:

    loop_flg = True
    page = 1

    while loop_flg:

        url = "https://da.lib.shimane-u.ac.jp/content/ja/search/p/" + \
            str(page)+"?place_name="+place

        print("page\t" + url)

        sleep(1)

        r = requests.get(url, verify=False)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(r.text, "lxml")

        arr_e = soup.find_all(class_="show-detail-btn")

        if len(arr_e) > 0:
            for e in arr_e:
                id = e.get("data-url").split("/")[-1]
                href = "https://da.lib.shimane-u.ac.jp/content/ja/"+id

                ff(href)

        else:
            loop_flg = False

        page += 1

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

for manifest in manifest_arr:
    writer.writerow([manifest])

f.close()
