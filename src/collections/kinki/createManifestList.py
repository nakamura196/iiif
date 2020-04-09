import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep

if __name__ == '__main__':

    flg = True
    page = 1

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    while flg:

        url = "https://kda.clib.kindai.ac.jp/rarematerials/search?sf=title_a&rows=30&vt=&page=" + str(page)

        print("page\t" + url)

        sleep(1)

        html = urllib.request.urlopen(url)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")

        arr_a = soup.find_all(class_="view-link")

        if len(arr_a) > 0:
            for element_a in arr_a:
                tmp_str = element_a.get("href").split("/")
                id = tmp_str[len(tmp_str) - 1]
                manifest = "https://kda.clib.kindai.ac.jp/rarematerials/iiif/rarematerials/" + id + "/manifest.json"

                manifest_arr.append(manifest)

        else:
            flg = False

        page += 1

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    print(len(manifest_arr))

    f.close()
