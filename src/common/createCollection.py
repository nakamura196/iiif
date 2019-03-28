import json

map = dict()
map["codh"] = "日本古典籍データセット（国文研所蔵）CODH配信"
map[
    "kkz"] = "General Library in the University of Tokyo, Council for Promotion of Study of Daizokyo, and the SAT Daizōkyō Text Database Committee"
map["koyasan"] = "Copyright (C) Koyasan University All Rights Reserved."
map["kyoto"] = "Kyoto University Rare Materials Digital Archive"
map["nakano"] = "中野区立図書館"
map["nijl"] = "National Institute of Japanese Literature"
map["ninjal"] = "National Institute for Japanese Language and Linguistics"
map[
    "saga"] = "This property is owned by Saga University Library and is used for regionological research by The Center for Regional Culture and History, Saga University, Japan. "
map["shimane"] = "Shimane University Library Digital Archive Collection"
map["toyo"] = "NII / Toyo Bunko Digital Archives"
map["zuzoubu"] = "大蔵出版(Daizo shuppan) and SAT大蔵経テキストデータベース研究会(SAT Daizōkyō Text Database Committee) "
map["khirin"] = "National Museum of Japanese History"
map["ndl"] = "国立国会図書館 National Diet Library, JAPAN"
map["kinki"] = "Images Copyright Kindai University Central Library"
map["keio"] = "慶應義塾大学メディアセンター Keio University Libraries"
map["utda"] = "The University of Tokyo"
map["ueda"] = "上田市"
map["hiraga"] = "The University of Tokyo"
map["kyushu"] = "Kyushu University"
map["okayama"] = "岡山県立記録資料館"
map["utarchives"] = "UTArchives Digital Archive by The University of Tokyo"
map["chiba"] = "c-arc Chiba University Academic Resource Collections by Chiba University"
map["okinawa"] = "Okinawa Prefectural Library"
map["north-china-railway"] = "Digital Archive of North China Railway by Center for Open Data in the Humanities"
map["dch"] = "Digital Cultural Heritage by The University of Tokyo"
map["saga_pref"] = "Saga Prefectural Library Database by Saga Prefectural Library"
map["kansai"] = "Kansai University Open Research Center for Asian Studies"

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
