from novelty.celery import app
from blog.models import Rate
from bs4 import BeautifulSoup as bs
import requests

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
'accept': '*/*',
}


def func():
    session = requests.Session()
    URL = 'https://minfin.com.ua/currency/'
    html = session.get(URL, headers=headers)

    if html.status_code == 200:
        soup = bs(html.content, 'html.parser')
        table = soup.find('table', class_='mfcur-table-lg-currency')
        trs = table.find_all('tr', class_=None)

        items = []
        for tr in trs:
            items.append({
                'name': tr.find('a', class_=None).get_text(),
                'NBU': tr.find('span', class_='mfcur-nbu-full-wrap'),
            })
        items.pop(0)
        for item in items:
            item['NBU'] = float(str(item['NBU'])[35:41])
        return items
