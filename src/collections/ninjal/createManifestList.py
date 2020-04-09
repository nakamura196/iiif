import urllib.request
from bs4 import BeautifulSoup
import csv

def scrape_for_page(url):
    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    arr_a = soup.find_all("a")

    for element_a in arr_a:
        link = element_a.get("href")

        if "manifest.json" in link:
            manifest_arr.append(link)


if __name__ == '__main__':

    manifest_arr = []

    output_path = "data/manifest_list.csv"

    scrape_for_page("https://dglb01.ninjal.ac.jp/ninjaldl/iiif_list.php")

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Manifest"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    print(len(manifest_arr))

    f.close()
