import datetime

from facebook_scraper import get_posts
from time import sleep
import pandas as pd
# import csv


def scrape(n):
    while True:
        try: # Check if fbID is in the CSV
            df = pd.read_csv('FB_list.csv', index_col='Name')
            x = df.loc[n] #If this stage fails, the except block runs
            print(x)
            for post in get_posts(n, pages=1): #Run facebook_scrapper
                latest_url = post['post_url']
                print("Latest URL: " + latest_url)
                df = pd.read_csv('FB_list.csv')
                old_url_list = df.loc[df['Name'] == n, 'URL']
                print("Old URL: " + old_url_list)
                for old_url in old_url_list:
                    if latest_url == old_url:
                        print("Nothing's changed")
                        break
                    else:
                        print("New post URL for " + n + " " + latest_url)
                        df2 = df.replace({'URL':{old_url : latest_url}}) #write new URL to csv
                        df2.to_csv('FB_list.csv', index=False) #write new URL to csv
                        break
                break #facebook_scrapper usually gives two results, so this prevents the second result from being looped.

        except KeyError: #If they fbID does not exist, add it into the CSV
            print("Not in the list")
            df = pd.read_csv('FB_list.csv')
            df2 = df.append({
                'Name' : n,
                'Date added' : datetime.date.today()
            },ignore_index=True)
            df2.to_csv('FB_list.csv', index= False)
            print("CSV updated")
            df = pd.read_csv('FB_list.csv')
            print(df2)
            break

        else:
            print("else block ran")
            break
scrape("najibrazak")
scrape("limguaneng.malaysia")

