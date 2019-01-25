import csv
import sys
import argparse


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'collection_name',
        action='store',
        type=str,
        help='collection_name')

    return parser.parse_args(args)


def get_properties():
    with open("data/properties.csv", 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばしたい時

        properties = {}

        for row in reader:
            properties[row[0]] = row[1]

        return properties


def get_omeka_ids(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばしたい時

        oids = {}

        for row in reader:
            if row[2] == "":
                properties[row[0]] = row[1]

        return properties


if __name__ == "__main__":
    args = parse_args()

    collection_name = args.collection_name

    path = "data"

    csv_path = path + "/" + collection_name + "/metadata.csv"

    output_path = path + "/" + collection_name + "/insert.sql"
    fo = open(output_path, 'w')  # 書き込みモードで開く

    properties = get_properties()

    oids = get_omeka_ids(path + "/" + collection_name + "/oids.csv")

    column_map = {}

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)

        row_count = 0

        for row in reader:

            if row_count == 0:

                for i in range(1, len(row)):
                    term = row[i]
                    if term in properties:
                        column_map[i] = term

            else:

                id = row[0]

                if id not in oids:
                    print(id)
                    continue

                oid = oids[id]

                for column_count in column_map:
                    term = column_map[column_count]
                    pid = properties[term]
                    value = row[column_count]

                    if value == "":
                        continue

                    value = value.replace("'", "\\'")

                    if term == "dcterms:isPartOf" or term == "dcterms:rights" or term == "dcterms:relation" or term == "rdfs:seeAlso" or term == "dcterms:references" or term == "foaf:thumbnail":
                        sql = "INSERT INTO `value` (`id`, `resource_id`, `property_id`, `value_resource_id`, `type`, `lang`, `value`, `uri`) VALUES (NULL, '" + str(
                            oid) + "', '" + str(pid) + "', NULL, 'uri', NULL, NULL, '" + value + "');"
                    else:
                        sql = "INSERT INTO `value` (`id`, `resource_id`, `property_id`, `value_resource_id`, `type`, `lang`, `value`, `uri`) VALUES (NULL, '" + str(
                            oid) + "', '" + str(pid) + "', NULL, 'literal', '', '" + value + "', NULL);"
                    fo.write(sql + "\n")  # 引数の文字列をファイルに書き込む

            row_count += 1

    fo.close()  # ファイルを閉じる
