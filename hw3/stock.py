import requests
from bs4 import BeautifulSoup


def stock(code):
    code = str(code)
    stock_url = "https://tw.stock.yahoo.com/class-quote?sectorId=40&exchange=TAI"
    stock_resp = requests.get(stock_url)

    if stock_resp.status_code != 200:
        print("Invalid URL::", stock_resp.url)
        print("code:", stock_resp.status_code)
        exit()

    stock_soup = BeautifulSoup(stock_resp.text, features="html.parser")

    stock_list = stock_soup.select_one(
        "#main-1-ClassQuotesTable-Proxy > div > div.ClassQuotesTable > div.table-body > div > div > ul"
    )

    # Find all the stock items in the list
    stock_items = stock_list.select("li")

    for stock_item in stock_items:
        stock_name = stock_item.select_one(
            r"div > div.D\(f\) > div.Fxs\(0\) > div > div.Lh\(20px\)"
        )
        stock_code = stock_item.select_one(
            r"div > div.D\(f\) > div.Fxs\(0\) > div > div.D\(f\)"
        )
        stock_info = stock_item.select(
            r"div.Fxg\(1\)"
        )

        if code+'.TW' == stock_code.text:
            print('股名：', stock_name.text)
            print('代號：', stock_code.text)
            print('股價：', stock_info[0].text)
            print('漲跌：', stock_info[1].text)
            print('漲跌幅：', stock_info[2].text)
            print('-' * 30) 

print(stock(2329))
