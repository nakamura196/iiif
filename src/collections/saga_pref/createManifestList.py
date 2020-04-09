import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

manifest_arr = []


def scrape_for_page(base_url):
    flg = True

    page = 1

    while flg:

        sleep(1)

        url = base_url + str(page)

        print("page\t" + url)

        page += 1

        r = requests.get(url, verify=False)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(r.text, "lxml")

        arr_a = soup.find_all("a")

        if len(arr_a) > 0:
            tmp_flg = False
            for element_a in arr_a:
                href = element_a.get("href")
                tmp = href.split("iiifviewer/?uid=")
                if len(tmp) > 1:
                    manifest = "https://www.sagalibdb.jp/"+tmp[1]+"/manifest"
                    # print(manifest)
                    tmp_flg = True
                    if manifest not in manifest_arr:
                        manifest_arr.append(manifest)

            if not tmp_flg:
                flg = False

        else:
            flg = False


output_path = "data/manifest_list.csv"

url_array = [
    "https://www.sagalibdb.jp/kaiga/index.php?num=100&page=",
    "https://www.sagalibdb.jp/azazu/index.php?num=100&page=",
    "https://www.sagalibdb.jp/tikei/index.php?num=100&page=",
    "https://www.sagalibdb.jp/kingendai/index.php?num=100&page=",
    "https://www.sagalibdb.jp/ezu/index.php?num=100&page="
]

for url in url_array:

    scrape_for_page(url)

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

for manifest in manifest_arr:
    writer.writerow([manifest])

f.close()
