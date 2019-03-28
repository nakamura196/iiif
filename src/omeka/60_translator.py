from pykakasi import kakasi

import csv

kakasi = kakasi()

count = 0

fo = open('data/title.sql', 'w')  # 書き込みモードで開く

text = ""

with open('data/title.csv', 'r') as f:
    reader = csv.reader(f)

    for row in reader:

        if count % 100 == 0:
            print(count)

        count = count + 1

        id = row[1]
        title = row[6]

        kakasi.setMode('J', 'K')
        kakasi.setMode('H', 'K')
        kakasi.setMode('K', 'K')

        conv = kakasi.getConverter()

        try:
            k = conv.do(title)
            k = k.replace("'", "\\\'")
            k_sql = "INSERT INTO `value` (`id`, `resource_id`, `property_id`, `value_resource_id`, `type`, `lang`, `value`, `uri`) VALUES ('0', '" + id + "', '219', NULL, 'literal', '', '" + k + "', NULL);\n"
            text += k_sql

        except:
            print(title)
            k = title

        kakasi.setMode('H', 'a')
        kakasi.setMode('K', 'a')
        kakasi.setMode('J', 'a')

        conv = kakasi.getConverter()

        try:
            a = conv.do(title)
            a = a.replace("'", "\\\'")
            a_sql = "INSERT INTO `value` (`id`, `resource_id`, `property_id`, `value_resource_id`, `type`, `lang`, `value`, `uri`) VALUES ('0', '" + id + "', '229', NULL, 'literal', '', '" + a + "', NULL);\n"
            text += a_sql
        except:
            a = title

        if count > 180:
            break

fo.write(text)
fo.close()  # ファイルを閉じる
