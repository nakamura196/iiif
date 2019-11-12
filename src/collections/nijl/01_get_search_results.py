import urllib.request
from bs4 import BeautifulSoup
import csv
import requests
import os
import json
import time

page = 0
flg = True

while flg:

    url = "https://kotenseki.nijl.ac.jp/app/ws/search/?q={%22bool%22:{%22must%22:[{%22bool%22:{%22should%22:[{%22bool%22:{%22must%22:[{%22exists%22:{%22field%22:%22s.iid%22}},{%22multi_match%22:{%22fields%22:[%22s.pubflg%22],%22query%22:%221%22}}]}},{%22multi_match%22:{%22fields%22:[%22t.link.s.searchFlg%22,%22t.iiiflink.s.searchFlgIIIF%22],%22query%22:%221%22}}]}}]}}&ag={%22d_kansha_terms%22:{%22terms%22:{%22field%22:%22d.kansha.keyword%22,%22size%22:2147483647}},%22d_bshubetsu_terms%22:{%22terms%22:{%22field%22:%22d.bshubetsuh.keyword%22,%22size%22:2147483647}},%22d_tshomeih_terms%22:{%22terms%22:{%22field%22:%22d.tshomeih.keyword%22,%22size%22:2147483647}},%22d_wkeyword_terms%22:{%22terms%22:{%22field%22:%22d.wkeyword.keyword%22,%22size%22:2147483647}},%22d_chosha_terms%22:{%22terms%22:{%22field%22:%22d.chosha.keyword%22,%22size%22:2147483647}},%22d_mchosha_terms%22:{%22terms%22:{%22field%22:%22d.mchosha.keyword%22,%22size%22:2147483647}},%22d_cryakushoh_terms%22:{%22terms%22:{%22field%22:%22d.cryakushoh.keyword%22,%22size%22:2147483647}},%22t_imgtag_d_tag_terms%22:{%22terms%22:{%22field%22:%22t.imgtag.d.tag.keyword%22,%22size%22:2147483647}},%22d_shomeih_terms%22:{%22terms%22:{%22field%22:%22d.shomeih.keyword%22,%22size%22:2147483647}},%22d_tchoshah_terms%22:{%22terms%22:{%22field%22:%22t.Work.auth.d.tchoshah.keyword%22,%22size%22:2147483647}},%22en.d_kansha_terms%22:{%22terms%22:{%22field%22:%22en.d.kansha.keyword%22,%22size%22:2147483647}},%22en.d_bshubetsu_terms%22:{%22terms%22:{%22field%22:%22en.d.bshubetsuh.keyword%22,%22size%22:2147483647}},%22en.d_tshomeih_terms%22:{%22terms%22:{%22field%22:%22en.d.tshomeih.keyword%22,%22size%22:2147483647}},%22en.d_wkeyword_terms%22:{%22terms%22:{%22field%22:%22en.d.wkeyword.keyword%22,%22size%22:2147483647}},%22en.d_chosha_terms%22:{%22terms%22:{%22field%22:%22en.d.chosha.keyword%22,%22size%22:2147483647}},%22en.d_mchosha_terms%22:{%22terms%22:{%22field%22:%22en.d.mchosha.keyword%22,%22size%22:2147483647}},%22en.d_cryakushoh_terms%22:{%22terms%22:{%22field%22:%22en.d.cryakushoh.keyword%22,%22size%22:2147483647}},%22en.t_imgtag_d_tag_terms%22:{%22terms%22:{%22field%22:%22en.t.imgtag.d.tag.keyword%22,%22size%22:2147483647}},%22en.d_shomeih_terms%22:{%22terms%22:{%22field%22:%22en.d.shomeih.keyword%22,%22size%22:2147483647}},%22en.tchoshah_terms%22:{%22terms%22:{%22field%22:%22en.t.Work.auth.d.tchoshah.keyword%22,%22size%22:2147483647}}}&hl={%22require_field_match%22:false,%22fields%22:{%22d.tshomeih%22:{%22cls%22:%22nx-highlight-color%22},%22d.wkeyword%22:{%22cls%22:%22nx-highlight-color%22},%22d.mchosha%22:{%22cls%22:%22nx-highlight-color%22},%22s.seiritsu%22:{%22cls%22:%22nx-highlight-color%22},%22d.mshomeihoka%22:{%22cls%22:%22nx-highlight-color%22},%22d.cryakushoh%22:{%22cls%22:%22nx-highlight-color%22},%22d.callno%22:{%22cls%22:%22nx-highlight-color%22},%22d.kansha%22:{%22cls%22:%22nx-highlight-color%22},%22d.kanshahoka%22:{%22cls%22:%22nx-highlight-color%22},%22d.satsusu%22:{%22cls%22:%22nx-highlight-color%22},%22d.keitai%22:{%22cls%22:%22nx-highlight-color%22},%22d.zanketsu%22:{%22cls%22:%22nx-highlight-color%22},%22d.bshubetsu%22:{%22cls%22:%22nx-highlight-color%22},%22en.d.tshomeih%22:{%22cls%22:%22nx-highlight-color%22},%22en.d.mchosha%22:{%22cls%22:%22nx-highlight-color%22},%22en.d.mshomeihoka%22:{%22cls%22:%22nx-highlight-color%22},%22en.d.cryakushoh%22:{%22cls%22:%22nx-highlight-color%22},%22en.d.kanshahh%22:{%22cls%22:%22nx-highlight-color%22},%22en.d.kanshahoka%22:{%22cls%22:%22nx-highlight-color%22}}}&sz=100&fr="+str(page*100)+"&sr={%22s.wid.keyword%22:{%22order%22:%22acs%22}}&sg={%22sg.perhaps%22:{%22text%22:%22%22,%22term%22:{%22field%22:%22t.suggest.s.suggest.keyword%22}}}&id=biblio.search&tp=search"

    page += 1

    opath = "data/result/"+str(page).zfill(5)+".json"

    if not os.path.exists(opath):

        print(page)

        fw = open(opath, 'w')
        
        headers = {"content-type": "application/json"}

        time.sleep(0.5)

        r = requests.get(url, headers=headers)

        
        data = r.json()
            
        hits = data["hits"]["hits"]

        json.dump(hits, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        if len(hits) == 0:
            flg = False

