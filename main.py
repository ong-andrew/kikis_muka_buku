import datetime
import requests
from facebook_scraper import get_posts
from time import sleep
import pandas as pd
from discord_webhook import DiscordWebhook


def scrape(n):
    while True:
        try:  # Check if fbID is in the CSV
            df = pd.read_csv('/path/to/FB_list.csv', index_col='Name')
            x = df.loc[n]  # If this stage fails, the except block runs
            for post in get_posts(n, pages=1):  # Run facebook_scrapper
                latest_url = post['post_url']
                post_id = post['post_id']
                user_id = post['user_id']
                latest_post = post['text'][:150]
                print("Latest URL: " + latest_url)
                df = pd.read_csv(
                    '/path/to/FB_list.csv')  # initialise df again without calling index_col
                old_url_list = df.loc[df['Name'] == n, 'URL']
                print("Old URL: " + old_url_list)
                for old_url in old_url_list:  # this removes the index column
                    if latest_url == old_url:
                        print("Nothing's changed")
                        break
                    else:
                        print("New post URL for " + n + " " + latest_url)
                        df2 = df.replace({'URL': {old_url: latest_url}})  # replace old URL to df
                        df2.to_csv('/path/to/FB_list.csv', index=False)  # write new df (URL) to csv

                        #the only way to get the preview out is using this URL format
                        w3_url = "https://facebook.com/story.php?story_fbid=" + post_id + "&id=" + user_id

                        #Send to the mattermost incoming webhook
                        headers = {'Content-Type': 'application/json', }
                        values = '{ "text": "' + str(n) + " posted " + str(latest_post) + "\n Link: " + str(w3_url) + '"}'
                        response = requests.post(
                            'https://xxx.cloud.mattermost.com/xxx',
                            headers=headers, data=values)
                        break
                break  # facebook_scrapper usually gives two results, so this prevents the second result from being looped.
            break  # This is needed to prevent else block from running

        except KeyError:  # If they fbID does not exist, add it into the CSV
            print("Not in the list")
            df = pd.read_csv('/path/to/FB_list.csv')
            df2 = df.append({
                'Name': n,
                'Date added': datetime.date.today()
            }, ignore_index=True)
            df2.to_csv('FB_list.csv', index=False)
            print("CSV updated")
            print(df2)
            break

        else:
            print("else block ran")
            break


scrape("najibrazak")
