from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from config import *


def save_single_article(url:str) -> dict:
    resp = urlopen(url)
    parser = 'lxml'
    bs = BeautifulSoup(resp.read(), parser)    
    article_dict = {}
    article_title_class = 'article__header__title-in js-slide-title'
    article_overview_class = 'article__text__overview'
    article_image_class = 'article__main-image__image'

    article_title = bs.find_all('h1', {'class': article_title_class})[0].contents[0].split('\n')[1].strip()
    article_overview = bs.find_all('div', {'class': article_overview_class})[0].contents[1].contents[0].get_text().replace('«\u200e', '')
    article_image = bs.find_all('img', {'class': article_image_class})[0]['src']

    dt_format = '%Y-%m-%d'
    today = datetime.now().strftime(format=dt_format)

    article_dict['title'] = article_title
    article_dict['overview'] = article_overview
    article_dict['link'] = url
    article_dict['created_at'] = today
    article_dict['image_url'] = article_image

    return article_dict