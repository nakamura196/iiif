import json

map = dict()
map["codh"] = "日本古典籍データセット（国文研所蔵）CODH配信"
map[
    "kkz"] = "General Library in the University of Tokyo, Council for Promotion of Study of Daizokyo, and the SAT Daizōkyō Text Database Committee"
map["koyasan"] = "Copyright (C) Koyasan University All Rights Reserved."
map["kyoto"] = "Kyoto University Rare Materials Digital Archive"
map["nakano"] = "中野区立図書館"
map["ninj"] = "http://www.ninjal.ac.jp/"
map[
    "saga"] = "This property is owned by Saga University Library and is used for regionological research by The Center for Regional Culture and History, Saga University, Japan. "
map["shimane"] = "Shimane University Library Digital Archive Collection"
map["toyo"] = "NII / Toyo Bunko Digital Archives"
map["zuzoubu"] = "大蔵出版(Daizo shuppan) and SAT大蔵経テキストデータベース研究会(SAT Daizōkyō Text Database Committee) "
map["khirin"] = "National Museum of Japanese History"
map["ndl"] = "国立国会図書館 National Diet Library, JAPAN"
map["kinki"] = "Images Copyright Kindai University Central Library"
map["keio"] = "慶應義塾大学メディアセンター Keio University Libraries"
map["nijl"] = "国文学研究資料館"
map["utda"] = "東京大学総合図書館 General Library in the University of Tokyo, JAPAN"
map["ueda"] = "上田市"
map["hiraga"] = "東京大学柏図書館 Kashiwa Library in the University of Tokyo, JAPAN"
map["kyushu"] = "Kyushu University Library Collections"
map["okayama"] = "岡山県立記録資料館"
map["utarchives"] = "東京大学文書館 / The University of Tokyo Archives, JAPAN"
map["chiba"] = "Chiba University Library"

universe = dict()
universe["@context"] = "http://iiif.io/api/presentation/2/context.json"
universe["@id"] = "https://nakamura196.github.io/iiif/data/collection/collection.json"
universe["@type"] = "sc:Collection"
universe["label"] = "IIIF Collections in Japan"
collections = []
universe["collections"] = collections

output_path = "../../docs/data/collection/collection.json"

for type in map:
    collection = dict()
    collections.append(collection)
    collection["@id"] = "https://nakamura196.github.io/iiif/data/collection/collections/" + type + ".json"
    collection["@type"] = "sc:Collection"
    collection["label"] = map[type]

fw = open(output_path, 'w')
json.dump(universe, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
