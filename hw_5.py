import json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as s_exc
from pymongo import MongoClient


url = 'https://www.mvideo.ru/'

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
mvideo = db.mvideo

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get(url)

new_items = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..")
actions = ActionChains(driver)
actions.move_to_element(new_items).perform()

while True:
    try:
        button = new_items.find_element_by_xpath(".//a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']")
        button.click()
    except s_exc.NoSuchElementException:
        break

all_items = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..")
items = all_items.find_elements_by_xpath(".//li[contains(@class, 'gallery-list-item')]")
for item in items:
    new_product = {}
    url = item.find_element_by_tag_name('a').get_attribute('href')
    name = item.find_element_by_tag_name('a').get_attribute('data-track-label')
    price = float(json.loads(item.find_element_by_tag_name('a').get_attribute('data-product-info'))['productPriceLocal'])

    new_product['url'] = url
    new_product['name'] = name
    new_product['price'] = price

    mvideo.update_one({'url': url}, {'$set': new_product}, upsert=True)

for item in mvideo.find({}):
    pprint(item)
