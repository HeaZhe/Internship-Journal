import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
# from django.http import HttpResponse
from celery import shared_task
from script.scripts.Stocks import get_stocks
from script.scripts.NTUT_Posts import get_ntut_posts
from script.models import News, Stocks, NTUT_Posts
import logging
logger = logging.getLogger(__name__)

@shared_task
def fetch_news():
    driver = webdriver.Chrome()
    driver.get("https://www.setn.com/ViewAll.aspx")
    wait = WebDriverWait(driver, 10)

    news_list_XPATH = '/html/body/form/div[2]/div/div[2]/div[3]'

    def scroll_to_bottom():
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
            current_scroll = driver.execute_script("return window.scrollY + window.innerHeight")
            if current_scroll >= scroll_height:
                break

    def get_news_count():
        news_elements = driver.find_elements(By.XPATH, f'{news_list_XPATH}/div')
        return len(news_elements)

    previous_news_count = 0

    while True:
        scroll_to_bottom()
        news_count = get_news_count()
        print(f"Current news count: {news_count}, Previous news count: {previous_news_count}")

        if news_count == previous_news_count:
            break
        previous_news_count = news_count

        for news_number in range(1, news_count + 1):
            try:
                news = wait.until(
                    EC.visibility_of_element_located((By.XPATH, f'{news_list_XPATH}/div[{news_number}]/div/h3/a'))
                )
                news_url = news.get_attribute('href')
                print(f"Fetching news: {news.text}, URL: {news_url}")

                if News.objects.filter(url=news_url).exists():
                    print(f"News already exists in database: {news_url}")
                    break

                content_resp = requests.get(news_url)
                if content_resp.status_code != 200:
                    print(f"Invalid URL: {content_resp.url}, Status code: {content_resp.status_code}")
                    continue

                content_soup = BeautifulSoup(content_resp.text, features="html.parser")

                if news_url.startswith("https://star.setn.com/"):
                    content_div = content_soup.find('div', id='mainContent').find('div').find('div', id='ckuse').find('article').find_all('p')
                    datetime_div = content_soup.find('div', id='mainContent').find('div').find('div', class_="newsPage newsTime printdiv").find('time').text
                    datetime_obj = datetime.strptime(datetime_div, '%Y/%m/%d %H:%M')
                else:
                    content_div = content_soup.find('form').find('div', id='contFix').find('div').find('div', class_='col-lg-9 col-md-8 col-sm-12 contLeft').find('div', class_='page-text').find('div', id='ckuse').find('article').find_all('p')
                    datetime_div = content_soup.find('form').find('div', id='contFix').find('div').find('div', class_='col-lg-9 col-md-8 col-sm-12 contLeft').find('div', class_='content').find('div', class_='page-title-text').find('time').text
                    datetime_obj = datetime.strptime(datetime_div, '%Y/%m/%d %H:%M:%S')

                content = '\n'.join(p.text for p in content_div)
                taipei_tz = pytz.timezone('Asia/Taipei')
                datetime_obj = taipei_tz.localize(datetime_obj)
                formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S%z')

                if News.objects.filter(title=news.text).exists():
                    print(f"News with same title already exists: {news.text}")
                else:
                    News.objects.create(
                        title=news.text,
                        datetime=formatted_datetime,
                        content=content,
                        url=news_url
                    )
                    print(f"News saved: {news.text}")

            except Exception as e:
                print(f"Error fetching news {news_number}: {e}")

    driver.quit()
    return '新聞爬蟲完成'

@shared_task
def fetch_stocks():
    stocks = get_stocks()
    for stock in stocks:
        # 去除逗号并转换为浮点数
        def parse_float(value):
            try:
                return float(value.replace(',', ''))
            except ValueError:
                return None

        stock_data = {
            'name': stock['stock_name'],
            'code': stock['stock_code'],
            'price': None if parse_float(stock['stock_price']) == '-' else parse_float(stock['stock_price']),
            'change': None if stock['stock_change'] == '-' else stock['stock_change'],
            'change_percent': None if stock['stock_change_rate'] == '-' else stock['stock_change_rate']
        }

        obj, created = Stocks.objects.update_or_create(
            fetch_at=stock['fetch_at'],
            defaults=stock_data
        )

        if created:
            logger.info(f"創建新股票記錄: {stock['stock_name']}")
        else:
            logger.info(f"更新股票記錄: {stock['stock_name']}")
    return '股票爬蟲完成'


@shared_task
def fetch_ntut_posts():
    post = get_ntut_posts()

    post_data = {
        'context': post['Context']
    }

    obj, created = NTUT_Posts.objects.update_or_create(
        context=post['Context'],
        defaults=post_data
    )
    if created:
        logger.info(f"創建新校園公告記錄")
    else:
        logger.info(f"校園公告記錄未更新")
    pass