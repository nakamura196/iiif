# IIIF Discovery in Japan

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

https://www.kanzaki.com/works/2016/pub/image-annotator?u=https://nakamura196.github.io/iiif/data/collection/collection.json

***

### 各コレクションの取得プログラム（順次追加中）
```
src/collections
│
└───collection_A
|   │   createManifestList.py
|   └───data
|       │   manifest_list.csv（取得したIIIF Manifestの一覧）
|       │   ...
│
└───collection_B
|   │   createManifestList.py
|   └───data
|       │   manifest_list.csv
|       │   ...
```

***

