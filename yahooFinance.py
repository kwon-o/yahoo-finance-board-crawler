import time
import datetime
import pandas as pd
import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, URL, START=datetime.datetime.now().strftime("%Y-%m-%d")):
        self.URL = URL
        self.START = datetime.datetime.strptime(START, '%Y-%m-%d')
        self.END = datetime.datetime.now()
        self.result = []
        self.title = ''
        self.boardNum = 0

    def main(self):
        source = requests.get(self.URL).text
        soup = BeautifulSoup(source, "html.parser")
        self.boardNum = int(soup.find("div", class_="threadAbout").h1.a["href"].split('/')[-1])
        self.title = soup.find("span", itemprop="name").text.split(' ')[0]
        """
        クロールしたい期間のループを設定
        """
        loop = (self.END - self.START).days
        for i in range(loop + 1):
            self.yahooFinanceCrawler()
            self.boardNum -= 1

        self.saveCsv(self.result)

    def yahooFinanceCrawler(self):
        """
        seleniumでページを更新し、
        全ページのコメントをクローリング
        """
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
                comInfo = key.find("p", class_="comWriter").text.split('\n')
                if len(comInfo) == 5:
                    comTime = comInfo[3]
                else:
                    comTime = comInfo[2]
            except AttributeError:
                continue
            if len(comTime) <= 12:
                comTime = '2021-' + comTime.replace('月', '-').replace('日', '')
            else:
                comTime = comTime.replace('年', '-').replace('月', '-').replace('日', '')
            comTime = datetime.datetime.strptime(comTime, '%Y-%m-%d %H:%M')
            comText = key.find("p", class_="comText").text.replace('\n', '')
            comNum = key.find("span", class_="comNum").text
            comNum = re.findall("\d+", comNum)[0]
            # index = 銘柄コード(6文) + 掲示板番号(4文) + コメント番号(4文)
            index = self.title.zfill(6) + str(self.boardNum).zfill(4) + comNum.zfill(4)
            row = [index, comTime, comText]
            self.result.append(row)

    def saveCsv(self, result):
        now = datetime.datetime.now().strftime("%Y%m%d")
        csv_name = now + "_" + self.title + ".csv"
        result = pd.DataFrame(result, columns=['index', 'time', 'text'])
        result.to_csv(csv_name, index=False, encoding='utf-8')


if __name__ == '__main__':
    '''
    url = 掲示板のリンク
    START = 指定する日から今日までの掲示板のコメントをクロール
    '''
    # url = 'https://finance.yahoo.co.jp/cm/message/1998407/ffc7pjbf6q3t2a'
    url = 'https://finance.yahoo.co.jp/cm/message/1023337/e9faca58a5ca59a5c0a5ca5afbbxbft'
    crawling = Crawler(url, START="2021-02-08")
    crawling.main()
