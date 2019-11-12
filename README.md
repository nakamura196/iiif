# IIIF Discovery in Japan 関連リポジトリ

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

***

### 利用上の注意

* 各コレクションのデータ利用にあたっては、公開元の利用条件をご確認ください。
* 取得時期や方法、抽出漏れやエラーにより、各コレクションで公開されているIIIF Manifestをすべて取得できていない場合があります。

***

### IIIF Collectionのディレクトリ構造

https://github.com/nakamura196/iiif/tree/master/docs/data/collection

```
docs/data/collection
|   collection.json（本ファイルがすべてのコレクションを包含したIIIF Collectionです）
|   
└───collections
    │   collection_A.json
    │   collection_B.json
    │   collection_C.json
    │   ...

```

***

### コレクションの一覧

<dl>
<dt>chiba</dt>
<dd>Chiba University Library</dd>
<dt>nakano</dt>
<dd>中野区立図書館</dd>
<dt>keio</dt>
<dd>慶應義塾大学メディアセンター Keio University Libraries</dd>
<dt>saga</dt>
<dd>This property is owned by Saga University Library and is used for regionological research by The Center for Regional Culture and History, Saga University, Japan. </dd>

<dt>ndl</dt>
<dd>国立国会図書館 National Diet Library, JAPAN</dd>

<dt>toyo</dt>
<dd>NII / Toyo Bunko Digital Archives</dd>

<dt>koyasan</dt>
<dd>Copyright (C) Koyasan University All Rights Reserved.</dd>

<dt>kyushu</dt>
<dd>Kyushu University Library Collections</dd>

<dt>nijl</dt>
<dd>国文学研究資料館</dd>

<dt>kinki</dt>
<dd>Images Copyright Kindai University Central Library</dd>

<dt>shimane</dt>
<dd>Shimane University Library Digital Archive Collection</dd>

<dt>ninj</dt>
<dd>http://www.ninjal.ac.jp/</dd>

<dt>utda</dt>
<dd>東京大学</dd>

<dt>okayama</dt>
<dd>岡山県立記録資料館</dd>

<dt>kyoto</dt>
<dd>Kyoto University Rare Materials Digital Archive</dd>

<dt>khirin</dt>
<dd>National Museum of Japanese History</dd>

<dt>codh</dt>
<dd>日本古典籍データセット（国文研所蔵）CODH配信</dd>

<dt>ueda</dt>
<dd>上田市</dd>

</dl>

***

### 各コレクションの取得プログラム（順次追加中）
```
src/collections
│
└───collection_A
|   │   createManifestList.py
|   └───data
|       │   manifest_list.csv（取得したIII Manifestの一覧）
|       │   ...
│
└───collection_B
|   │   createManifestList.py
|   └───data
|       │   manifest_list.csv
|       │   ...
```

***

