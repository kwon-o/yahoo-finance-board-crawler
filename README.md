# Yahooファイナンス掲示板クローラー (yahoo-finance-board-crawler)
seleniumを活用した掲示板のコメントを取得するクローラです。<br>
銘柄コード、日付、コマンドの内容(Full Text)をクローリングします。<br>
学習用で使用してください。<br>
クローリングしたデータの著作権は[Yahooファイナンス](https://finance.yahoo.co.jp/)にあります。
* Python(>=3.7.7)
* コーディングのスタイルガイドはPEP8を準拠しています。
* selenium, BeautifulSoup, requestsライブラリが必要です。

``` python
$ pip install beautifulsoup4
$ pip install requests
$ pip install selenium
```

## 基本設定
1. seleniumを使うために自分が利用しているブラウザのバージョンと合うselenium WebDriverをダウンロードします。
  * [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  * [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
  * [Firefox](https://github.com/mozilla/geckodriver/releases)
  * [Safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)
2. ダウンロードしたWebDriverをyahooFinance.pyと同じ場所に配置します。
  * 配置例
  ```
  yahoo_finance_jp
  ├── yahooFinance.py
  └── chromedriver.exe
  ```
---
## 作成中<
