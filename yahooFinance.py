import time
import datetime
import pandas as pd
import requests
from selenium import webdriver
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, URL, FROM=datetime.datetime.now().strftime("%Y-%m-%d")):
        self.URL = URL
        self.FROM = datetime.datetime.strptime(FROM, '%Y-%m-%d')
        self.TO = datetime.datetime.now()
        self.result = []
        self.title = ''
        self.comInfo = ''
        self.comTime = ''
        self.comText = ''
        self.boardNum = 0
        self.cnt = 0

    def main(self):
        source = requests.get(self.URL).text
        soup = BeautifulSoup(source, "html.parser")
        self.boardNum = int(soup.find("div", class_="threadAbout").h1.a["href"].split('/')[-1])
        self.title = soup.find("span", itemprop="name").text.split(' ')[0]

        loop = (self.TO - self.FROM).days
        while loop >= 0:
            self.yahooFinanceCrawler()
            self.boardNum -= 1
            loop -= 1

        self.saveCsv(self.result)

    def yahooFinanceCrawler(self):
        driver = webdriver.Chrome(executable_path='chromedriver')
        driver.get(url=self.URL + "/" + str(self.boardNum))

        SCROLL_PAUSE_SEC = 2
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

        for key in hotKeys:
            try:
                self.comInfo = key.find("p", class_="comWriter").text.split('\n')
                if len(self.comInfo) == 5:
                    self.comTime = self.comInfo[3]
                else:
                    self.comTime = self.comInfo[2]
            except AttributeError:
                continue
            self.comText = key.find("p", class_="comText").text.replace('\n', '')
            self.cnt += 1
            row = [self.cnt, self.comTime, self.comText]
            self.result.append(row)

    def saveCsv(self, result):
        now = datetime.datetime.now().strftime("%Y%m%d")
        csv_name = now + "_" + self.title + ".csv"
        result = pd.DataFrame(result, columns=['index', 'time', 'text'])
        result.to_csv(csv_name, index=False, encoding='utf-8')


if __name__ == '__main__':
    # url = 'https://finance.yahoo.co.jp/cm/message/1998407/ffc7pjbf6q3t2a'
    url = 'https://finance.yahoo.co.jp/cm/message/1023337/e9faca58a5ca59a5c0a5ca5afbbxbft'
    crawling = Crawler(url, FROM="2021-02-07")
    crawling.main()
