import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep

if __name__ == '__main__':

    output_path = "data/manifest_list.csv"

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    url_list = ["https://iiif.ll.chiba-u.jp/main/koisho.shtml", "https://iiif.ll.chiba-u.jp/main/engeisho.shtml",
                "https://iiif.ll.chiba-u.jp/main/machinoke.shtml", "https://iiif.ll.chiba-u.jp/main/fungi.shtml"]

    for url in url_list:

        sleep(1)

        html = urllib.request.urlopen(url)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")

        li_list = soup.find("ol").find_all("li")

        for li in li_list:
            manifest_uri = li.find_all("a")[2].get("href")
            writer.writerow([manifest_uri])

    f.close()
