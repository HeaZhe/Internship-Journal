import requests
from bs4 import BeautifulSoup

url = "https://www.facebook.com/taipeitech1912"
resp = requests.get(url)
stock_soup = BeautifulSoup(resp.text, features="html.parser")

stock_list = stock_soup.select(
    r"#mount_0_0_\/B > div > div > div > div > div > div > div.x9f619 > div > div.x1uvtmcs > div > div > div > div.x92rtbv > div > i"
)

print(stock_list)

#mount_0_0_\/B > div > div:nth-child(1) > div > div:nth-child(5) > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div.x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm > div > i