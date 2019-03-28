import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def scrape_for_page(path):
    flg = True

    print("page\t" + url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(open(path), "lxml")

    arr_a = soup.find_all("a")

    if len(arr_a) > 0:
        for element_a in arr_a:
            href = element_a.get("href")
            tmp = href.split("iiifviewer/?uid=")
            if len(tmp) > 1:
                manifest = "https://www.sagalibdb.jp/"+tmp[1]+"/manifest"
                if manifest not in manifest_arr:
                    manifest_arr.append(manifest)

    else:
        flg = False

    return flg


if __name__ == '__main__':

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    url_array = [
        "/Users/nakamura/git/iiif/src/collections/saga/data/azazu.html",
        "/Users/nakamura/git/iiif/src/collections/saga/data/ezu.html",
        "/Users/nakamura/git/iiif/src/collections/saga/data/kaiga.html",
        "/Users/nakamura/git/iiif/src/collections/saga/data/kingendai.html",
        "/Users/nakamura/git/iiif/src/collections/saga/data/tikei.html"]

    for url in url_array:

        scrape_for_page(url)

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    f.close()
