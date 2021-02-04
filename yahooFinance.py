from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd

now = datetime.datetime.now().strftime("%Y%m%d")

URL = 'https://finance.yahoo.co.jp/cm/message/1998407/ffc7pjbf6q3t2a'

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=URL)

SCROLL_PAUSE_SEC = 3
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(SCROLL_PAUSE_SEC)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
hotKeys = soup.find_all("div", class_="comment")

result = []
cnt = 0
csv_name = now+"_com.csv"
hotKeys.reverse()
for key in hotKeys:
    try:
        comTime = key.find("p", class_="comWriter").text.split('\n')[2]
    except AttributeError :
        continue
    comText = key.find("p", class_="comText").text
    cnt += 1
    row = [cnt, comTime, comText]
    result.append(row)

result = pd.DataFrame(result, columns=['index', 'time', 'text'])
result.to_csv(csv_name, index=False, encoding='utf-8')