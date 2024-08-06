import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz


def get_news():
    driver = webdriver.Chrome()
    driver.get("https://www.setn.com/ViewAll.aspx")
    wait = WebDriverWait(driver, 10)

    news_list_XPATH = '/html/body/form/div[2]/div/div[2]/div[3]'

    def scroll_to_bottom():
        while True:
            # 滾動到頁面底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 等待3秒以確保頁面加載完成
            time.sleep(3)
            # 檢查是否到達頁面底部
            scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
            current_scroll = driver.execute_script("return window.scrollY + window.innerHeight")
            if current_scroll >= scroll_height:
                break

    def get_news_count():
        news_elements = driver.find_elements(By.XPATH, f'{news_list_XPATH}/div')
        return len(news_elements)

    news_titles = []  # 使用集合來存儲新聞標題，避免重複
    news_content = []  # 使用集合來存儲新聞內容，避免重複
    news_datetime = []  # 使用集合來存儲新聞日期，避免重複
    previous_news_count = 0

    while True:
        # scroll_to_bottom()
        news_count = get_news_count()

        # 如果新聞數量沒有變化，則認為所有新聞已加載
        if news_count == previous_news_count:
            break
        previous_news_count = news_count

        for news_number in range(1, news_count + 1):
            try:
                news = wait.until(
                    EC.visibility_of_element_located((By.XPATH, f'{news_list_XPATH}/div[{news_number}]/div/h3/a'))
                )
                news_url = news.get_attribute('href')

                content_resp = requests.get(news_url)

                if content_resp.status_code != 200:
                    print("content_resp Invalid url:", content_resp.url)
                    print("code:", content_resp.status_code)
                    exit()

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

                news_titles.append(news.text)
                news_content.append(content)
                news_datetime.append(formatted_datetime)
            except Exception as e:
                print(f"Error fetching news {news_number}: {e}")
    driver.quit()

    return news_titles, news_content, news_datetime