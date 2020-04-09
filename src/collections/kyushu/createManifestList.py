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

    arr_a = soup.find_all(class_="result-book-title")

    if len(arr_a) > 0:
        for element_a in arr_a:
            link = "https://catalog.lib.kyushu-u.ac.jp" + element_a.find("a").get("href")

            scrape_for_item(link)



    else:
        flg = False

    return flg


def scrape_for_item(url):
    print("item\t" + url)

    sleep(1)

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    uv = soup.find(class_="uv")
    if uv != None:
        manifest = uv.get("data-uri")
        print(manifest)
        manifest_arr.append(manifest)


if __name__ == '__main__':

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    url_array = [
        "https://catalog.lib.kyushu-u.ac.jp/opac_search/?lang=0&amode=22&opkey=B158641765030518&cmode=0&place=&list_sort=0&list_disp=500&start="]

    for base_url in url_array:

        loop_flg = True
        page = 1

        while loop_flg:
            url = base_url + str(500 * (page - 1) + 1)

            loop_flg = scrape_for_page(url)

            page += 1

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    f.close()
