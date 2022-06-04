from GoogleNews import GoogleNews
import os
import tweepy as tw
from pandas import ExcelWriter
import csv 
from time import sleep 
from selenium.common.exceptions import NoSuchElementException 
import selenium
import time
from PIL import Image
import io
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from facebook_scraper import get_profile
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import datetime
import requests
from datetime import datetime

def Google(name):
    date_lst =[]
    title_lst =[]
    media_lst =[]
    datetime_lst =[]
    desc_lst =[]
    link_lst =[]
    img_lst =[]


    def show_routine(results):
        for num,page in enumerate(results):
            #print(f"{num}. {page['date']} - {page['title']} - {page['media']} - {page['datetime']} - {page['desc']} - {page['link']} - {page['img']}  ")
            date_lst.append(page['date'])
            title_lst.append(page['title'])
            media_lst.append(page['media'])
            datetime_lst.append(page['datetime'])
            desc_lst.append(page['desc'])
            link_lst.append(page['link'])
            img_lst.append(page['img'])

    ### MAIN

    # Setup the research
    keywords=name
    period='10d'
    google_news = GoogleNews(lang='en',period=period)
    google=GoogleNews(lang='en',period=period)

    # Results from news.google.com
    google_news.get_news(keywords)
    results_gnews=google_news.results(sort=True)
    show_routine(results_gnews)

    # Results from google.com
    google.search(keywords)
    results_google=google.results(sort=True)
    show_routine(results_google)



    df = pd.DataFrame(
        {'date':date_lst, 
        'title':title_lst,
        'media':media_lst,
        'datetime':datetime_lst,
        'desc':desc_lst,
        'link':link_lst,
        'img':img_lst
        })
    #print(df)
    df.to_csv("google.csv", index = False, header = True)
    return (df)

def Twitter(name):
    consumer_key        = 'sx6llfl3gRsOBNw3y7VVKSQT7'
    consumer_secret     = 'DSZiX1mHEsKTcT7JMnahQY2dPC4lQNV21hkorPszWkz8D2Q5oH'
    access_token        = '998804133288144901-pPeZ4V3B9jmEDhhVbvML9tYAMgXy55A'
    access_token_secret = 'AdqyikZTdUaStqYAF4hKzCpRwSiLHWveOjlygarnrFIBY'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth,wait_on_rate_limit = True)

    search_words = name
    new_search   = search_words + " -filter:retweets"

    tweets = tw.Cursor(api.search_tweets, 
                    q                = new_search,
                    result_type      = "mixed",
                    lang             = "id",
                    count            = 100,
                    include_entities = True,
                    since_id         = "2020-01-01").items(500)

    users_locs = [[tweet.created_at,
                tweet.author.screen_name,
                tweet.author.name,
                tweet.text,
                tweet.retweet_count,
                tweet.favorite_count,
                tweet.user.location] for tweet in tweets]

    tweet_text = pd.DataFrame(data = users_locs, 
                            columns = ["date",
                                        "user",
                                        "name",
                                        "text",
                                        "retweet",
                                        "favorite",
                                        "location"])

    tweet_text.to_csv("twitter.csv", index = False, header = True)
    #tweet_text.to_excel("{}.xlsx".format(search_words), index = False)
    #print(tweet_text)
    return tweet_text

def YouTube(name):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    text= name
    driver.get('https://www.youtube.com/results?search_query='+ text)
    time.sleep(3) 
    contents = driver.find_elements(By.XPATH, '//*[@id="dismissible"]')
    


    duration_lst=[]
    title_lst=[]
    views_lst=[]
    uploaded_lst=[]
    channel_lst=[]
    description_lst=[]
    for content in contents:
        try:
            duration=content.text.split('\n')[0]
            title=content.text.split('\n')[1]
            views=content.text.split('\n')[2]
            uploaded=content.text.split('\n')[3]
            channel=content.text.split('\n')[4]
            description=content.text.split('\n')[5]
        except:
            continue
        duration_lst.append(duration)
        title_lst.append(title)
        views_lst.append(views)
        uploaded_lst.append(uploaded)
        channel_lst.append(channel)
        description_lst.append(description)

    df = pd.DataFrame(
        {'Title':title_lst, 
        'Description':description_lst,
        'Duration':duration_lst,
        'Views':views_lst,
        'Channel':channel_lst,
        'Uploaded':uploaded_lst
        })
    df=df[df['Description']!='New']
    indx=df[df['Duration'] == 'People also watched'].index.values[0]
    df=df[:df.index.get_loc(indx)]

    df.to_csv("youtube.csv", index= False, header= True)
    return df


def Facebook(name):
    # Initialize dataframe to scrape Facebook post
    pro_df_full = pd.DataFrame(columns = [])
    text = name
    profile = get_profile(text, cookies="cookie.txt")

    fb_pro_df = pd.DataFrame.from_dict(profile, orient='index')
    fb_pro_df = fb_pro_df.transpose()
    pro_df_full = pro_df_full.append(fb_pro_df)
    pro_df_full.head(50)
    pro_df_full.to_csv("facebook.csv", index= False)
    #print(pro_df_full)

    return pro_df_full

def Facebook_Posts(name, user):
    # set options as you wish
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    with open('facebook_credentials.txt') as file:
        EMAIL = file.readline().split('"')[1]
        PASSWORD = file.readline().split('"')[1]
    

    #print(PASSWORD)
        
    browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    browser.get("http://facebook.com")
    browser.maximize_window()
    wait = WebDriverWait(browser, 30)
    email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
    email_field.send_keys(EMAIL)
    pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
    pass_field.send_keys(PASSWORD)
    pass_field.send_keys(Keys.RETURN)
    time.sleep(5)
    text=name
    browser.get('https://www.facebook.com/search/posts/?q='+ text) # once logged in, free to open up any target page
    time.sleep(5)

    #scroll down
    #increase the range to sroll more
    #example: range(0,10) scrolls down 650+ images
    for j in range(0,10):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    time.sleep(5)

    soup=BeautifulSoup(browser.page_source,"html.parser")
    all_posts=soup.find_all("div",{"class":"rq0escxv l9j0dhe7 du4w35lb hybvsw6c io0zqebd m5lcvass fbipl8qg nwvqtn77 k4urcfbm ni8dbmo4 stjgntxs sbcfpzgs"})

    Name=[]
    Time=[]
    Post=[]
    for content in all_posts:
        try:
            Name.append(content.text.split('·')[0])
            Time.append(content.text.split('·')[1])
            Post.append(content.text.split('·')[2].split('Shared with Public')[1])
        except:
            continue

    browser.quit()
    Time=Time[:len(Post)]
    Name=Name[:len(Post)]

    df = pd.DataFrame(
        {'Name': Name,
        'Time': Time,
        'Post': Post
        })
    #print(df)
    
    shortDate = datetime.today().strftime("%d_%m_%Y-%H:%M:%S")
    print(shortDate)
    df.to_csv("facebook_csv/"+text+"-"+ str(shortDate) +'-'+user+".csv", index=False)
    

    all_photo=soup.find_all("img")
    image_name= text
    #print(all_photo)
    i=0
    for photo in all_photo:
        i+=1
        link = photo['src']
        Name=f'scrape_image/{image_name} {i}.jpg'
        #print((image_name+{i}).format(i))
        with open(Name, 'wb') as f:
            try:
                img = requests.get(link)
                f.write(img.content)
            except:
                continue

    return df


if __name__ == "__main__":
#     google("covid")
#     twitter("covid")
#     youtube("covid")
#     Facebook("Shaon.ComputerGeek")
     Facebook_Posts("opus technology limited", "partho")