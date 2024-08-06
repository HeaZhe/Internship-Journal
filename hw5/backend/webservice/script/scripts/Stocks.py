import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_stocks():
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
    stocks_list = []

    fetch_at = datetime.now().isoformat()  # Get the current timestamp

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
        stock_data = {
            'stock_name': stock_name.text if stock_name else None,
            'stock_code': stock_code.text if stock_code else None,
            'stock_price': stock_info[0].text if len(stock_info) > 0 else None,
            'stock_change': stock_info[1].text if len(stock_info) > 1 else None,
            'stock_change_rate': stock_info[2].text if len(stock_info) > 2 else None,
            'fetch_at': fetch_at
        }
        stocks_list.append(stock_data)

    return stocks_list

