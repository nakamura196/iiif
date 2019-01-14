from selenium import webdriver
import time
import re
from selenium.webdriver.support.ui import Select
import os


def save(html):
    ids = re.findall('https://www.library.pref.okinawa.jp/item/index-(.*?).html', html)

    if len(ids) > 0:
        file = "data/html/" + ids[0] + ".html"
        if not os.path.exists(file):
            Html_file = open(file, "w")
            Html_file.write(html)
            Html_file.close()


driver = webdriver.Chrome()

driver.get('https://www.library.pref.okinawa.jp/archive/index.html')

driver.find_element_by_class_name("menu02").click()

driver.find_element_by_name("submit_btn_searchDetailAllAr").click()

# 普通にエレメントを取得する
color_element = driver.find_element_by_name('opt_oder')

# 取得したエレメントをSelectタグに対応したエレメントに変化させる
color_select_element = Select(color_element)

# 選択したいvalueを指定する
color_select_element.select_by_value('0')

driver.find_element_by_name("submit_btn_sort").click()

driver.find_element_by_class_name("link-image").click()

save(driver.page_source)

for i in range(2, 1001):
    time.sleep(1)
    if i % 50 == 0:
        print(i)

    driver.find_element_by_class_name("next").click()

    save(driver.page_source)

driver.quit()
