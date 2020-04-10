import openpyxl
import requests
import pandas as pd
import csv

df_size = pd.read_csv("data/json_list.csv", header=0)
manifest_arr = []
for i in range(len(df_size.index)):
    if i % 10 == 0:
        print(str(i+1) + "/" + str(len(df_size.index)))
    uri = df_size.iloc[i, 0]
    data = requests.get(uri).json()
    if "relation" in data:
        manifest = data["relation"]
        manifest_arr.append(manifest)

output_path = "data/manifest_list.csv"

f = open(output_path, 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerow(["Manifest"])

for manifest in manifest_arr:
    writer.writerow([manifest])

f.close()