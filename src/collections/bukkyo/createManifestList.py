import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

manifest_arr = []

def func2(base_url):

    print(base_url)

    sleep(1)

    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "lxml")

    a_arr = soup.find(class_="title-data-area").find_all("a")
    for a in a_arr:
        url = a.get("href")
        id = url.split("/")[4]
        manifest = "https://bird.bukkyo-u.ac.jp/collections/iiif/manifests/"+id+"-manifest.json"
        manifest_arr.append(manifest)
    

def scrape_for_page(base_url):
    flg = True

    print("page\t" + base_url)

    sleep(1)

    r = requests.get(base_url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(r.text, "lxml")

    a_arr = soup.find_all(class_="title-thumbnail-caption")

    if len(a_arr) > 0:
        for a in a_arr:
            url = a.get("href")
            func2(url)
    else:
        flg = False
    
    return flg


output_path = "data/manifest_list.csv"

base_url = "https://bird.bukkyo-u.ac.jp/collections/wp-content/themes/2018/content-titlelist-ajax.php?orderby=date&order=DESC&paged="

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
