import re
import csv
import glob

files = glob.glob("data/html/*.html")

output_path = "data/manifest_list_all_licenses.csv"

manifest_arr = []

for file in files:

    filename = file.split("/")[-1].replace(".html", "")
    manifest = "https://www.library.pref.okinawa.jp/item/manifest/" + filename + "/manifest.json"

    f = open(file)
    data = f.read()  # ファイル終端まで全て読んだデータを返す
    f.close()

    images = re.findall('<img src="/winj/img/pc/(.*?)"', data)

    if len(images) > 0:

        license = "0"
        image = images[0]

        if image == "10_by.png":
            license = "http://creativecommons.org/licenses/by/4.0/"

        manifest_arr.append([manifest, license])

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest", "License"])

for manifest in manifest_arr:
    writer.writerows([manifest])

f.close()
