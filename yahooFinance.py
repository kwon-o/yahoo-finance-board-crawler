import time
import datetime
import pandas as pd
import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, url, START=datetime.datetime.now().strftime("%Y-%m-%d")):
        self.URL = url
        self.START = datetime.datetime.strptime(START, '%Y-%m-%d')
        self.END = datetime.datetime.now()
        self.allComment = []
        self.stockCode = ''
        self.boardNum = 0

    def main(self):
        self.getStockCodeAndBoardNum()

        for BoardLoop in range((self.END - self.START).days + 1):
            self.yahooFinanceBoardCrawler()
            self.boardNum -= 1

        self.saveCsv()

    def getStockCodeAndBoardNum(self):
        mainBoardHtml = self.getHtml(self.URL)
        mainBoardHtmlParse = self.htmlParser(mainBoardHtml)
        self.boardNum = int(mainBoardHtmlParse.find("div", class_="threadAbout").h1.a["href"].split('/')[-1])
        self.stockCode = mainBoardHtmlParse.find("span", itemprop="name").text.split(' ')[0]

    @staticmethod
    def getHtml(url: str) -> str:
        return requests.get(url).text

    @staticmethod
    def htmlParser(html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    def yahooFinanceBoardCrawler(self):  # seleniumでページを更新し、全ページのコメントをクローリング
        driver = webdriver.Chrome(executable_path='chromedriver')
        driver.get(url=self.URL + "/" + str(self.boardNum))

        SCROLL_PAUSE_SEC = 2  # 待機時間(秒)

        last_height = driver.execute_script("return document.body.scrollHeight")  # 初期ブラウザの高さ
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(SCROLL_PAUSE_SEC)
            new_height = driver.execute_script("return document.body.scrollHeight")  # スクロールを下した後の高さ
            if new_height == last_height:  # スクロールを下した後の高さ = 現在の高さになるまでループ(下るページがもうない)
                break
            last_height = new_height  # 高さをスクロールを下した後の高さに更新

        subBoardHtml = driver.page_source
        subBoardHtmlParse = self.htmlParser(subBoardHtml)

        allCommentHtml = subBoardHtmlParse.find_all("div", class_="comment")[:-1]  # 最後は管理者のコメントなので除外

        for eachCommentHtml in allCommentHtml:
            try:  # 広告を処理するための例外処理
                timeLocationCheck = eachCommentHtml.find("p", class_="comWriter").text.split('\n')
                # 時間の位置には2つのパタンがある
                if len(timeLocationCheck) == 5:
                    comTime = timeLocationCheck[3]
                else:
                    comTime = timeLocationCheck[2]
            except AttributeError:
                continue
            # 掲示した日付が今年の場合の例）2/16 10:00
            # 掲示した日付が去年前の場合の例）2020/12/31 10:00
            # したがって、今年に掲示されたコメントには年度を追加する。
            if len(comTime) <= 12:
                comTime = '2021-' + comTime.replace('月', '-').replace('日', '')
            else:
                comTime = comTime.replace('年', '-').replace('月', '-').replace('日', '')
            comTime = datetime.datetime.strptime(comTime, '%Y-%m-%d %H:%M')
            comText = eachCommentHtml.find("p", class_="comText").text.replace('\n', '')
            comNum = eachCommentHtml.find("span", class_="comNum").text
            comNum = re.findall("\d+", comNum)[0]
            id = self.stockCode.zfill(6) + str(self.boardNum).zfill(4) + comNum.zfill(4)

            eachComment = [id, comTime, comText]
            self.allComment.append(eachComment)

    def saveCsv(self):
        now = datetime.datetime.now().strftime("%Y%m%d")
        csv_name = now + "_" + self.stockCode + ".csv"
        saveCsv = pd.DataFrame(self.allComment, columns=['id', 'time', 'comment'])
        saveCsv.to_csv(csv_name, index=False, encoding='utf-8')


if __name__ == '__main__':
    # url = 'https://finance.yahoo.co.jp/cm/message/1998407/ffc7pjbf6q3t2a'
    URL = 'https://finance.yahoo.co.jp/cm/message/1023337/e9faca58a5ca59a5c0a5ca5afbbxbft'
    crawling = Crawler(URL, START="2021-02-16")
    crawling.main()
