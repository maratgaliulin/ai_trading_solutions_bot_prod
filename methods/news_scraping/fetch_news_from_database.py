import sqlite3
from config import *

def fetch_news_from_database() -> list:
    conn = sqlite3.connect(db_directory)
    cursor = conn.cursor()
    all_news = cursor.execute(f'SELECT id, title, overview, link FROM rbc_news').fetchall()
    conn.commit()
    news_list_as_dict = []
    for single_news in all_news:
        single_news_dict = {}
        single_news_dict['id'] = single_news[0]
        single_news_dict['title'] = single_news[1]
        single_news_dict['overview'] = single_news[2]
        single_news_dict['link'] = single_news[3]

        news_list_as_dict.append(single_news_dict)

    conn.close()
    return news_list_as_dict