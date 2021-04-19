from facebook_scraper import get_posts
from time import sleep
import pandas
# import csv

df = pandas.read_csv('FB_list.csv')
print(df)

def scrape(n):
    for post in get_posts(n, pages=1):
        fb_post_url = post['post_url']
        # check against FB_list.csv
        if df[Name]
        print(fb_post_url)
        sleep(10)
        break


# scrape("najibrazak")
# scrape("limguaneng.malaysia")
