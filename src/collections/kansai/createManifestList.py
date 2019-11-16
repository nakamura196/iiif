import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def scrape_for_page(url):
    flg = True

    print("page\t" + url)

    sleep(1)

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    if soup.find(class_="view-content") == None:
        return False

    arr_a = soup.find(class_="view-content").find_all("a")

    if len(arr_a) > 0:
        for element_a in arr_a:

            manifest = "https://www.iiif.ku-orcas.kansai-u.ac.jp/iiif"+element_a.get("href")+"/manifest.json"

            if "hakuen_yinpu" in manifest:
                html = urllib.request.urlopen("https://www.iiif.ku-orcas.kansai-u.ac.jp/"+element_a.get("href"))

                # htmlをBeautifulSoupで扱う
                soup = BeautifulSoup(html, "html.parser")

                aas = soup.find_all("a")

                for a in aas:
                    href = a.get("href")
                    if "manifest.json" in href:
                        manifest = href
                        break


            else:
                manifest = "https://www.iiif.ku-orcas.kansai-u.ac.jp/iiif"+element_a.get("href").split("-")[0]+"/manifest.json"

            print(manifest)
            manifest_arr.append(manifest)

    else:
        flg = False

    return flg


if __name__ == '__main__':

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    url_array = [
        "https://www.iiif.ku-orcas.kansai-u.ac.jp/books?page=", 
        "https://www.iiif.ku-orcas.kansai-u.ac.jp/osaka_gadan?page=", 
        "https://www.iiif.ku-orcas.kansai-u.ac.jp/hakuen_bunko?page=", 
        "https://www.iiif.ku-orcas.kansai-u.ac.jp/hakuen_yinpu?page="
    ]

    for base_url in url_array:

        loop_flg = True
        page = 1

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
