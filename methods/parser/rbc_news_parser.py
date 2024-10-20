from urllib.request import urlopen
from urllib.request import HTTPHandler
from bs4 import BeautifulSoup
import time
import random
import sqlite3
from config import *

from .save_single_article import save_single_article
# from .save_the_image import save_the_image
import urllib3

def rbc_news_parser():
    txt_file_directory = './database/article_links.txt'
    url = 'https://www.rbc.ru/quote'    
    articles_list = []
    article_links = []
    all_attrs = []
    article_ids_list =  []
    resp = urlopen(url)
    parser = 'lxml'
    bs = BeautifulSoup(resp.read(), parser)    
    all_hrefs = list(bs.find_all('a'))
    for ref in all_hrefs:
        if ref.has_attr('href'):
            all_attrs.append(ref.attrs['href'])
    for a in all_attrs:
        if ('quote/news/article' in a) and ('?from=newsfeed' not in a):
            article_links.append(a)
    article_links = set(article_links)

    with open(txt_file_directory, 'r') as f:
        lines = f.readlines()
        set_from_file = set(lines[0].strip(',').split(','))
        
    if((article_links != set_from_file)):
        with open(txt_file_directory, 'w') as f:
            for el in article_links:
                f.writelines(el + ',')

        for lnk in article_links:
            random_no = random.randint(29, 61)
            single_article = save_single_article(lnk)
            articles_list.append(single_article)
            print(single_article, random_no)
            time.sleep(random_no)

        conn = sqlite3.connect(db_directory)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rbc_news")
        conn.commit()
        
        for i, article in enumerate(articles_list):
            cursor.execute(f"INSERT INTO rbc_news (id, title, overview, link, created_at, image) VALUES ({i}, '{article['title']}', '{article['overview']}', '{article['link']}', '{article['created_at']}', '{article['image_url']}')")
        conn.commit()
        # conn.close()

        # conn = sqlite3.connect(db_directory)
        # cursor = conn.cursor()

        # article_ids = cursor.execute(f'SELECT id, image FROM rbc_news').fetchall()
        # conn.commit()

        # for art_id in article_ids:
        #     article_ids_list.append([art_id[0], art_id[1]])
        
        conn.close()
        
        # for item in article_ids_list:
        #     save_the_image(item)
        #     random_no = random.randint(29, 61)
        #     time.sleep(random_no)
        #     print(item, random_no)
    print('It is done!')