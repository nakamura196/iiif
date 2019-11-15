import json

map = dict()
map["codh"] = "Center for Open Data in the Humanities"
map["koyasan"] = "高野山大学 Koyasan University"
map["kyoto"] = "京都大学 Kyoto University"
map["nakano"] = "中野区立図書館 Nakano City Library"
map["nijl"] = "国文学研究資料館 National Institute of Japanese Literature"
map["ninjal"] = "国立国語研究所 National Institute for Japanese Language and Linguistics"
map[
    "saga"] = "佐賀大学 Saga University"
map["shimane"] = "島根大学 Shimane University"
# map["toyo"] = "国立情報学研究所 / 東洋文庫 NII / Toyo Bunko"
map["khirin"] = "国立歴史民俗博物館 National Museum of Japanese History"
map["ndl"] = "国立国会図書館 National Diet Library"
map["kinki"] = "近畿大学 Kindai University"
# map["keio"] = "慶應義塾大学 Keio University"
map["utda"] = "東京大学 The University of Tokyo"
map["ueda"] = "上田市 Ueda City"
map["kyushu"] = "九州大学 Kyushu University"
map["okayama"] = "岡山県立記録資料館 Okayama Prefectural Archives"
map["chiba"] = "千葉大学 Chiba University"
map["okinawa"] = "沖縄県立大学 Okinawa Prefectural Library"
map["north-china-railway"] = "Center for Open Data in the Humanities"
map["saga_pref"] = "佐賀県立図書館 Saga Prefectural Library"
map["kansai"] = "関西大学 Kansai University"

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

    collection_uri = "https://nakamura196.github.io/iiif/data/collection/collections/" + type + ".json"
    if type == "utda":
        collection_uri = "https://nakamura196.github.io/portal_pro/data/collection.json"
    collection["@id"] = collection_uri
    collection["@type"] = "sc:Collection"
    collection["label"] = map[type]

fw = open(output_path, 'w')
json.dump(universe, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
