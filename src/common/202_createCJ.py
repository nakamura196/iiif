import yaml
import glob
import json

env_path = "../../.env.yml"
with open(env_path) as file:
    yml = yaml.load(file)

path = yml["json_dir"] + "/iiif/collections/*/*.json"
files = glob.glob(path)

manifests = []

license_check = {}

checks = [
    "",
    "http://kotenseki.nijl.ac.jp/page/usage.html",
    "http://rightsstatements.org/vocab/InC/1.0/",
    '<a href="http://dcollections.lib.keio.ac.jp/ja/about" target="_blank">http://dcollections.lib.keio.ac.jp/ja/about</a>',
    "佛教大学図書館<br/>Bukkyo University Library",
    "https://archives.koyasan-u.ac.jp/resource/license/license_ja.html"
]

for i in range(len(files)):
    file = files[i]

    if i % 10000 == 0:
        print("----------------")
        print("******\t"+str(i+1)+"/" + str(len(files)))

    with open(file) as f:
        data = json.load(f)

        if "@type" in data and data["@type"] == "sc:Manifest":

            license = ""

            if "license" in data:
                license = data["license"].strip()

            ##################

            if "thumbnail" not in data:

                sequences = data["sequences"]

                if len(sequences) == 0:
                    continue

                sequence = sequences[0]

                if "canvases" not in sequence:
                    continue

                canvases = sequences[0]["canvases"]

                if len(canvases) == 0:
                    continue

                canvas = canvases[0]
                resource = canvas["images"][0]["resource"]
                thumbnail = ""
                if "service" in resource:
                    thumbnail = resource["service"]["@id"] + \
                        "/full/200,/0/default.jpg"
                else:
                    thumbnail = canvas["thumbnail"]["@id"]

                if thumbnail != "":
                    data["thumbnail"] = thumbnail

            ##################

            if license not in license_check:
                print("----------------")
                print("'"+license+"'\t"+data["@id"])
                license_check[license] = 0

            license_check[license] += 1

            ##################

            if license not in checks:
                data.pop("sequences")

                if "structures" in data:
                    data.pop("structures")

                manifests.append(data)

collection = dict()
collection["@context"] = "http://iiif.io/api/presentation/2/context.json"
collection["@type"] = "sc:Collection"
collection["manifests"] = manifests

fw = open(yml["json_dir"] + "/iiif/cj.json", 'w')
json.dump(collection, fw, ensure_ascii=False,
          indent=4,
          sort_keys=True, separators=(',', ':'))

for license in license_check:
    print("----------------")
    print(license+"\t"+str(license_check[license]))

print("----------------")
print("manifest size:\t"+str(len(manifests)))
