import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
from urllib.parse import urljoin

output_path = "data/manifest_list.csv"

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

def func2(base_url):
    sleep(1)

    html = urllib.request.urlopen(base_url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    img_arr = soup.find_all(class_="img-fluid")

    for img in img_arr:
        src = img.get("src")
        try:
            id = src.split("/")[3].split(".")[0]
            manifest = "https://iiif.nichibun.ac.jp/IIIF/manifest/YSD/"+id+".json"
            writer.writerow([manifest])
        except Exception as e:
            print(e)
            


base_url = "https://iiif.nichibun.ac.jp/YSD/"

sleep(1)

html = urllib.request.urlopen(base_url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")

div_arr = soup.find_all(class_="border")

for div in div_arr:
    url2 = urljoin(base_url, div.find("a").get("href"))
    print(url2)
    func2(url2)

f.close()
