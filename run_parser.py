from methods.parser.rbc_news_parser import rbc_news_parser
import time

time_sleep = 86400


if (__name__ == '__main__'):
    while True:
        rbc_news_parser()
        time.sleep(time_sleep)
