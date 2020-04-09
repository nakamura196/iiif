import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep


def scrape_for_page(url):
    flg = True

    print("page\t" + url)

    sleep(1)

    try:

        html = urllib.request.urlopen(url)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")

        arr_a = soup.find_all(class_="hover-card")

        if len(arr_a) > 0:
            for element_a in arr_a:
                id = element_a.get("href").split("/")[4]
                manifest = "http://archive.nakano-library.jp/manifest/" + id + "_manifest.json"
                print("manifest\t" + manifest)
                manifest_arr.append(manifest)

        else:
            flg = False

    except urllib.error.URLError as e:
        flg = False

    return flg


if __name__ == '__main__':

    loop_flg = True
    page = 1

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    while loop_flg:
        url = "https://archive.nakano-library.jp/d_archives/page/" + str(page) + "/"

        loop_flg = scrape_for_page(url)
        print(loop_flg)

        page += 1

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    print(len(manifest_arr))

    f.close()
