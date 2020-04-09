import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import sys
sys.path.append('../../classes')
import notify

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

manifest_arr = []

def scrape_for_page(url):
    flg = True

    print("page\t" + url)

    sleep(1)

    r = requests.get(url,verify=False)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(r.text, "lxml")

    arr_a = soup.find_all(class_="m-card--type2")

    if len(arr_a) > 0:
        for a in arr_a:

            href = a.get("href")

            url = "https://khirin-ld.rekihaku.ac.jp" + href + ".json"
            
            print(url)
            manifest_arr.append(url)

            if len(manifest_arr) % 100 == 1:
                notify.Notify.send("khirin\t"+str(len(manifest_arr)), "../../classes/env.yml")

    else:
        flg = False

    return flg

output_path = "data/json_list.csv"

base_url = "https://khirin-ld.rekihaku.ac.jp/search/list?sf=s_a&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fchibaumachino&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnaruto_goto&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_kaken_medInterNationalExcange&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_kanzousiryou&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_nishikie&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_rekimin_a&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_rekimin_h&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_shuko&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2FsohanShiki&object=manifest&page="

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
