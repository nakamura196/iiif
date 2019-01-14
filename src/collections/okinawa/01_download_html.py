from selenium import webdriver
import time
import re

driver = webdriver.Chrome()

driver.get('https://www.library.pref.okinawa.jp/archive/index.html')

driver.find_element_by_class_name("menu02").click()

driver.find_element_by_name("submit_btn_searchDetailAllAr").click()

driver.find_element_by_class_name("link-image").click()

html = driver.page_source

ids = re.findall('https://www.library.pref.okinawa.jp/item/index-(.*?).html', html)

if len(ids) > 0:
    file = "data/html/" + ids[0] + ".html"
    Html_file = open(file, "w")
    Html_file.write(html)
    Html_file.close()

for i in range(2, 1001):
    time.sleep(1)
    driver.find_element_by_class_name("next").click()

    html = driver.page_source

    ids = re.findall('https://www.library.pref.okinawa.jp/item/index-(.*?).html', html)

    if len(ids) > 0:
        file = "data/html/" + ids[0] + ".html"
        Html_file = open(file, "w")
        Html_file.write(html)
        Html_file.close()

driver.quit()
