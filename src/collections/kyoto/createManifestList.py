import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep

if __name__ == '__main__':

    loop_flg = True
    page = 1

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    while loop_flg:

        url = "https://rmda.kulib.kyoto-u.ac.jp/search?keys=&page=" + str(page)

        print("page\t" + url)

        sleep(1)

        html = urllib.request.urlopen(url)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")

        arr_a = soup.find_all(class_="card-link")

        if len(arr_a) > 0:
            for element_a in arr_a:
                id = element_a.get("href").split("/")[2].upper()
                manifest = "https://rmda.kulib.kyoto-u.ac.jp/iiif/metadata_manifest/" + id + "/manifest.json"

                manifest_arr.append(manifest)

        else:
            loop_flg = False

        page += 1

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    f.close()
