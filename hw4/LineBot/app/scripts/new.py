import requests
from bs4 import BeautifulSoup
from datetime import datetime


def New():
    url = "https://www.setn.com/ViewAll.aspx"
    resp = requests.get(url)

    if resp.status_code != 200:
        print("context_resp Invalid url:", resp.url)
        print("code:",resp.status_code)
        exit()

    #建立爬取對象
    soup = BeautifulSoup(resp.text,features="html.parser")

    title_tag = soup.find('h3')
    a_tag = title_tag.find('a')

    title = title_tag.text
    href = a_tag.get('href')

    if href.startswith("http"):
        context_url = href
    else:
        context_url = f"https://www.setn.com{href}"

    context_resp = requests.get(context_url)

    if context_resp.status_code != 200:
        print("context_resp Invalid url:", context_resp.url)
        print("code:",context_resp.status_code)
        exit()

    context_soup = BeautifulSoup(context_resp.text,features="html.parser")

    if context_url.startswith("https://star.setn.com/"):
        content_div = context_soup.find('div', id='mainContent').find('div').find('div', id='ckuse').find('article').find_all('p')
        datetime_div = context_soup.find('div', id='mainContent').find('div').find('div', class_="newsPage newsTime printdiv").find('time').text
        datetime_obj = datetime.strptime(datetime_div, '%Y/%m/%d %H:%M')
        
    else:
        content_div = context_soup.find('form').find('div', id='contFix').find('div').find('div', class_='col-lg-9 col-md-8 col-sm-12 contLeft').find('div', class_='page-text').find('div', id='ckuse').find('article').find_all('p')
        datetime_div = context_soup.find('form').find('div', id='contFix').find('div').find('div', class_='col-lg-9 col-md-8 col-sm-12 contLeft').find('div', class_='content').find('div', class_='page-title-text').find('time').text
        datetime_obj = datetime.strptime(datetime_div, '%Y/%m/%d %H:%M:%S')

    formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

    # context_list = []
    # for p in content_div:
    #     context = p.text
    #     context_list.append(context)
    # context = ''.join(context_list)
    context = '\n'.join(p.text for p in content_div)

    return {'title':title, 'date':formatted_datetime, 'context':context}