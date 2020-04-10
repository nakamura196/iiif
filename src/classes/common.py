from hashlib import md5
import requests
import json

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


class Common:
    @classmethod
    def getId(self, manifest_uri):

        # スキーマの除去
        manifest_uri = manifest_uri.split("://")[1]

        # 大文字化
        manifest_uri = manifest_uri.upper()

        return md5(manifest_uri.encode('utf-8')).hexdigest()

    @classmethod
    def download(self, manifest_uri, output_path):
        r = requests.get(manifest_uri, verify=False)
        data = r.json()

        with open(output_path, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True,
                      separators=(',', ': '))

    
    @classmethod
    def getThubmnail(self, data):

        sequences = data["sequences"]

        if len(sequences) == 0:
            return None

        sequence = sequences[0]

        if "canvases" not in sequence:
            return None

        canvases = sequences[0]["canvases"]

        if len(canvases) == 0:
            return None

        canvas = canvases[0]
        resource = canvas["images"][0]["resource"]
        thumbnail = ""
        if "service" in resource:
            thumbnail = resource["service"]["@id"] + \
                                    "/full/200,/0/default.jpg"
        else:
            thumbnail = canvas["thumbnail"]["@id"]

        if thumbnail != "":
            return thumbnail
        else:
            return None