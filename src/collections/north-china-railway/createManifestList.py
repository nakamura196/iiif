import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep


def scrape_for_page(url):
    flg = True

    print("page\t" + url)

    sleep(1)

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    arr_a = soup.find_all(class_="thumbnail")

    if len(arr_a) > 0:
        for element_a in arr_a:
            id = element_a.get("href").split("/")[-1].split(".")[0]

            manifest = "http://codh.rois.ac.jp/north-china-railway/manifest/" + id + ".json"
            print(manifest)
            manifest_arr.append(manifest)



    else:
        flg = False

    return flg


if __name__ == '__main__':

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    url_array = [
        "http://codh.rois.ac.jp/north-china-railway/search/metadata?page="]

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
