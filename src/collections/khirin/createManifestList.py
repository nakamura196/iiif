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
            id = id.replace("/rdf/", "/manifests/") + ".json"
            manifest = "https://khirin-i.rekihaku.ac.jp" + id
            print(manifest)
            manifest_arr.append(manifest)

    else:
        flg = False

    return flg


def scrape_for_item(url):
    print("item\t" + url)

    sleep(1)

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")
    manifest = \
        soup.find(class_="thumbField").get("data-object").replace("https://khirin-i.rekihaku.ac.jp/mirador/?m=",
                                                                  "").split(
            "&")[0]

    manifest_arr.append(manifest)


if __name__ == '__main__':

    url_map = dict()
    url_map[
        "rekimin_h"] = "https://khirin-ld.rekihaku.ac.jp/search/list?sf=s_a&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_rekimin_h&object=CC"
    url_map[
        "rekimin_a"] = "https://khirin-ld.rekihaku.ac.jp/search/list?sf=s_a&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_rekimin_a&object=CC"
    url_map[
        "shuko"] = "https://khirin-ld.rekihaku.ac.jp/search/list?sf=s_a&graph=http%3A%2F%2Fkhirin-ld.rekihaku.ac.jp%2Frdf%2Fnmjh_shuko&object=CC"

    for key in url_map:

        output_path = "data/manifest_list_" + key + ".csv"

        base_url = url_map[key]

        loop_flg = True
        page = 1

        manifest_arr = []

        while loop_flg:
            url = base_url + "&page=" + str(page)

            loop_flg = scrape_for_page(url)

            page += 1

        f = open(output_path, 'w')

        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["Manifest"])

        for manifest in manifest_arr:
            writer.writerow([manifest])

        f.close()
