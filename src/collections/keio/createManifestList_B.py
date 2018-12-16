import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep


def scrape_for_group(url):
    print("group\t" + url)
    sleep(1)
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    arr_element_thumb = soup.find_all(class_="thumbnail")

    if len(arr_element_thumb) > 0:
        for element_thumb in arr_element_thumb:
            link = element_thumb.find("a").get("href")
            if link.find("http://dcollections.lib.keio.ac.jp") == -1:
                link = "http://dcollections.lib.keio.ac.jp" + link

            scrape_for_collection(link)


def scrape_for_collection(url):
    print("collection\t" + url)
    sleep(1)

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    arr_element_a = soup.find_all(class_="thumbnail-img")

    if len(arr_element_a) > 0:
        for element_a in arr_element_a:
            link = element_a.get("href")
            if link.find("http://dcollections.lib.keio.ac.jp") == -1:
                link = "http://dcollections.lib.keio.ac.jp" + link

            scrape_for_item(link)


def scrape_for_item(url):
    print("item\t" + url)
    sleep(1)

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    manifest = soup.find(class_="iiif-drag-drop-label").get("href")
    manifest_arr.append(manifest)


if __name__ == '__main__':

    output_path = "data/manifest_list_b.csv"

    manifest_arr = []

    url = "http://dcollections.lib.keio.ac.jp/ja"
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    arr_element_a = soup.find(class_="media-list").find_all("a")

    for element_a in arr_element_a:
        link = element_a.get("href")
        if link.find("explanation") == -1:

            # 「浮世絵」または「小山内」の場合のみ実行
            if link.find("ukiyoe") == -1 and link.find("osanai") == -1:
                continue

            scrape_for_group(link)

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    f.close()
