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
  /.
  ├── yahooFinance.py
  └── chromedriver.exe
  ```
---
## 使用方法
1. メインソースで実行する関数のパラメータは以下です。
``` python
if __name__ == '__main__':
    URL = 'https://finance.yahoo.co.jp/cm/message/1023337/e9faca58a5ca59a5c0a5ca5afbbxbft'
    crawling = Crawler(URL, START="2021-02-21")
    crawling.main()
```
 * URL：クローリングしたい掲示板のURL
 * START：クローリングを開始したい日付

2. 実行が終わると結果はcsvファイルに保存されます。csvの実行例は以下です。
```
index,time,text
02333700030046,2021-02-08 23:08:00,二階幹事長　森氏を擁護！　自民党員として情けない いい加減にしろ❗️   近くの憲政記念館で土下座しろ！
02333700030044,2021-02-04 22:13:00,釜萢理事　今日のテレビ出演はよかったねできれば医療現場で従事してください
02333700030043,2021-02-03 12:23:00,日経平均は週足見るとまさに「節分天井、彼岸底」を絵にかいたようなチャートで来週から下がりそうな予感してますけど、ジャスダック・マザーズはまだある程度の高値をキープしそうですね。
02333700030042,2021-02-03 05:45:00,自民党国会議員の皆様　いろんな不祥事で離党とか処分を下しているがどこかの幹事長自身の責任を感じないのか憲政記念館の尾崎先生像に今一度拝礼したらどうだい　その像が大きく又は小さく診えるのか古賀誠先生　あなたの政界引退がこのような結果を招いたのではないのでしょうか
02333700030040,2021-02-01 08:33:00,"低すぎる日本の世帯年収中央値360万円、世界と比べてみたら酷すぎだった・・・【世帯平均年収は541万】【超格差社会】60,386 回視聴https://www.youtube.com/watch?v=oMNMHMWNRZU&t=184s"
02333700030039,2021-01-31 18:58:00,"【ひろゆき】オリンピックを実行すれば変異株を持った外国人が大量に入って来て最悪の事態になる9,887 回視聴•2021/01/28https://www.youtube.com/watch?v=Q0q0EFW-GYw"
...(省略)...
```

3. 制限事項
 * 優良株を対象に作ったクローラーなので、コメントが少ない掲示板の場合、日付の範囲は一致しないです。
 * Yahooファイナンスのトラフィックの負荷を防止するために掲示板全体をクロールする方法は止揚しました。
