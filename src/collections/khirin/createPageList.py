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

    arr_a = soup.find_all(class_="m-card--type2")

    if len(arr_a) > 0:
        for element_a in arr_a:
            id = element_a.get("href")
            # id = id.replace("/rdf/", "/manifests/") + ".json"
            manifest = "https://khirin-ld.rekihaku.ac.jp" + id
            print(manifest)
            manifest_arr.append(manifest)

    else:
        flg = False

    return flg


if __name__ == '__main__':


    output_path = "data/page_list.csv"

    base_url = "https://khirin-ld.rekihaku.ac.jp/search/list?imgOnly=true&sf=s_a&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fchibaumachino&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnaruto_goto&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_kaken_medInterNationalExcange&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_kanzousiryou&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_nishikie&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_rekimin_a&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_rekimin_h&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_shuko&object=mirador"

    loop_flg = True
    page = 1

    manifest_arr = []

    while loop_flg:
        url = base_url + "&page=" + str(page)

        loop_flg = scrape_for_page(url)

        page += 1

    f = open(output_path, 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["Page"])

    for manifest in manifest_arr:
        writer.writerow([manifest])

    f.close()
