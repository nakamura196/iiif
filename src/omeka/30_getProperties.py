import sys
import csv
import urllib.request, json
import argparse

flg = True
page = 1

fo = open("data/properties.csv", 'w')
writer = csv.writer(fo, lineterminator='\n')
writer.writerow(
    ["term", "id"])

while flg:
    url = "http://iiif2.dl.itc.u-tokyo.ac.jp/api/properties?page=" + str(page)
    print(url)

    page += 1

    response = urllib.request.urlopen(url)
    response_body = response.read().decode("utf-8")
    data = json.loads(response_body.split('\n')[0])

    if len(data) > 0:
        for i in range(len(data)):
            obj = data[i]

            writer.writerow([obj["o:term"], obj["o:id"]])

    else:
        flg = False

fo.close()
