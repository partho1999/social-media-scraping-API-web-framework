from GoogleNews import GoogleNews
import os
from cv2 import convertFp16
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
import snscrape.modules.twitter as sntwitter
import numpy as np
from datetime import date,datetime,timedelta


def Google(name,user):
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
        'Post':title_lst,
        'media':media_lst,
        'datetime':datetime_lst,
        'desc':desc_lst,
        'link':link_lst,
        'img':img_lst
        })
    #print(df)
    time_stamp = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
    print(time_stamp)
    path= str(time_stamp)+'-'+ name +'-'+user+".csv"
    df['file_path'] = path
    
    df.to_csv(r"C:/Users/Administrator/Documents/social_media_django_2.0/project/google_csv/"+str(time_stamp)+'-'+ name +'-'+user+".csv", index = False, header = True)
    return (df)
#"/home/opus/Desktop/social_media_dj/project/facebook_csv/"+str(time_stamp)+'-'+ text +'-'+user+".csv"

def Twitter(n_tweets,name,user):
    """
    get a dataframe of tweets by search term
    ref: https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af
    """
    # Creating list to append tweet data to
    today = date.today()
    end_date = today.strftime("%Y-%m-%d")
    start_date = datetime.strftime(datetime.now() - timedelta(15), '%Y-%m-%d')
    tweets_list2 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{name} since:{start_date} until:{end_date}').get_items()):
        if i>n_tweets:
            break
        tweets_list2.append([tweet.date, tweet.id, tweet.content])

    # Creating a dataframe from the tweets list above
    tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet_Id', 'Post'])
    
    time_stamp = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
    print(time_stamp)
    path= str(time_stamp)+'-'+ name +'-'+user+".csv"
    tweets_df2['file_path'] = path
    print(tweets_df2)
    tweets_df2.to_csv(r"C:/Users/Administrator/Documents/social_media_django_2.0/project/twitter_csv/"+str(time_stamp)+'-'+ name +'-'+user+".csv", index=False, header = True)
  
    return tweets_df2

def YouTube(text,user):
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

    driver= webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    driver.get('https://www.youtube.com/results?search_query='+str(text))
    driver.maximize_window()


    # driver = webdriver.Chrome(executable_path="chromedriver.exe")
    # driver.get('https://www.youtube.com/results?search_query='+str(query))

    youtube_data = []

    # scrolling to the end of the page
    # https://stackoverflow.com/a/57076690/15164646
    while True:
        # end_result = "No more results" string at the bottom of the page
        # this will be used to break out of the while loop
        end_result = driver.find_element_by_css_selector('#message').is_displayed()
        driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
        # time.sleep(1) # could be removed
        print(end_result)

        # once element is located, break out of the loop
        if end_result == True:
            break

    print('Extracting results. It might take a while...')

    for result in driver.find_elements_by_css_selector('.text-wrapper.style-scope.ytd-video-renderer'):
        title = result.find_element_by_css_selector('.title-and-badge.style-scope.ytd-video-renderer').text
        link = result.find_element_by_css_selector('.title-and-badge.style-scope.ytd-video-renderer a').get_attribute('href')
        channel_name = result.find_element_by_css_selector('.long-byline').text
        channel_link = result.find_element_by_css_selector('#text > a').get_attribute('href')
        views = result.find_element_by_css_selector('.style-scope ytd-video-meta-block').text.split('\n')[0]

        try:
            time_published = result.find_element_by_css_selector('.style-scope ytd-video-meta-block').text.split('\n')[1]
        except:
            time_published = None

        try:
            snippet = result.find_element_by_css_selector('.metadata-snippet-container').text
        except:
            snippet = None

        try:
            if result.find_element_by_css_selector('#channel-name .ytd-badge-supported-renderer') is not None:
                verified_badge = True
            else:
                verified_badge = False
        except:
            verified_badge = None

        try:
            extensions = result.find_element_by_css_selector('#badges .ytd-badge-supported-renderer').text
        except:
            extensions = None
        print(verified_badge)

        time_stamp = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
        print(time_stamp)
        

        youtube_data.append({
            'title': title,
            'link': link,
            'channel': {'channel_name': channel_name, 'channel_link': channel_link},
            'views': views,
            'time_published': time_published,
            'snippet': snippet,
            'verified_badge': verified_badge,
            'extensions': extensions,
            'Post': title,
        })
    driver.quit()
    df = pd.DataFrame(youtube_data)
    time_stamp = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
    print(time_stamp)
    print(df)
    path= str(time_stamp)+'-'+ text +'-'+user+".csv"
    df['file_path'] = path
    df.to_csv(r"C:/Users/Administrator/Documents/social_media_django_2.0/project/youtube_csv/"+str(time_stamp)+'-'+ text +'-'+user+".csv", index= False, header= True)
    


    return df


def Facebook(name,user):
    # Initialize dataframe to scrape Facebook post
    pro_df_full = pd.DataFrame(columns = [])
    text = name
    profile = get_profile(text, cookies="C:/Users/Administrator/Documents/social_media_django_2.0/API/cookies.txt")

    fb_pro_df = pd.DataFrame.from_dict(profile, orient='index')
    fb_pro_df = fb_pro_df.transpose()
    #print(fb_pro_df)
    pro_df_full = fb_pro_df.copy()
    print(pro_df_full.head())
    # pro_df_full.head(50)
    time_stamp = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")
    print(time_stamp)
    path = str(time_stamp)+'-'+text+'-'+user+".csv",
    pro_df_full['pro_path'] =path
    pro_df_full.to_csv(r"C:/Users/Administrator/Documents/social_media_django_2.0/project/facebook_csv/"+str(time_stamp)+'-'+text+'-'+user+".csv", index=False)
    # #print(pro_df_full)

  
    #for collecting profile posts

    # set options as you wish
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    print("254")
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
    print("269")
    with open('C:/Users/Administrator/Documents/social_media_django_2.0/API/facebook_credentials.txt') as file:
        EMAIL = file.readline().split('"')[1]
        PASSWORD = file.readline().split('"')[1]
 
    print("274")
    #print(PASSWORD)
        
    browser = webdriver.Chrome(executable_path=r"C:/Users/Administrator/Documents/social_media_django_2.0/API/chromedriver.exe", options=options)
    browser.get("http://facebook.com")
    browser.maximize_window()
    wait = WebDriverWait(browser, 30)
    email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
    email_field.send_keys(EMAIL)
    pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
    pass_field.send_keys(PASSWORD)
    pass_field.send_keys(Keys.RETURN)
    print("286")
    time.sleep(5)

    text=name

    browser.get('https://www.facebook.com/'+ text) # once logged in, free to open up any target page
    print("292")
    time.sleep(5)

    #scroll down
    #increase the range to sroll more
    #example: range(0,10) scrolls down 650+ images
    for j in range(0,3):
        print(j)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    print("301")
    time.sleep(5)


    soup=BeautifulSoup(browser.page_source,"html.parser")
    posts=soup.find_all("div",{"class":"du4w35lb l9j0dhe7"})

    path = str(time_stamp)+'-'+text+'-'+'post'+'-'+user+".csv"
   

    postlist=[]
    namelist=[]
    pathlist=[]
    print("315")
    for post in posts:
        try:
            txt=post.find('div',{'class':'kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q'}).text
        except:
            txt='No Caption!'
        print(txt)
        postlist.append(txt)
    
    Imagelist=[]
    for post in posts:
        imagelink=[]
        img = post.find('img')
        if img is not None:
            imagelink.append(img['src'])
        print(imagelink)
        Imagelist.append(imagelink)
        print(img)
        namelist.append(text)
        pathlist.append(path)

    # for content in posts:
        
    #     #print(content.text)
    #     # postlist.append(content.text)
        

    dct={'ID_Name':namelist,'Pro_Posts':postlist, 'img_link':Imagelist, 'Post_Path':pathlist}
    df=pd.DataFrame(dct)
    print("Printing DF")
    print(df)
    df.to_csv(r"C:/Users/Administrator/Documents/social_media_django_2.0/project/facebook_csv/"+str(time_stamp)+'-'+text+'-'+'post'+'-'+user+".csv", index=False)
    
    horizontal_concat = pd.concat([df, pro_df_full], axis=1)
    print("horizontal print")
    print(horizontal_concat)
    try:
        all_photo=soup.find_all("img")
        image_name= text
        if not os.path.exists('scrape_image/'+image_name):
            os.makedirs('scrape_image/'+image_name,mode = 0o777)

        #print(all_photo)
        i=0
        for photo in all_photo:
            i+=1
            link = photo['src']
            #Name=f'scrape_image/{image_name}/{image_name} {i}.jpg'
            Name=f'scrape_image/{image_name}/{image_name} {i}.jpg'
            #print((image_name+{i}).format(i))
            
            with open(Name, 'wb') as f:
                try:
                    img = requests.get(link)
                    f.write(img.content)
                    #print(os.path.getsize(Name))
                except:
                    continue
    except:
        pass

    print('Returned df:',horizontal_concat)

    return horizontal_concat

def Facebook_Posts(text,user):
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

    with open('C:/Users/Administrator/Documents/social_media_django_2.0/API/facebook_credentials.txt') as file:
        EMAIL = file.readline().split('"')[1]
        PASSWORD = file.readline().split('"')[1]
    

    #print(PASSWORD)
        
    browser = webdriver.Chrome(executable_path=r"C:\Users\Administrator\Documents\social_media_django_2.0\API\chromedriver.exe", options=options)
    browser.get("http://facebook.com")
    browser.maximize_window()
    wait = WebDriverWait(browser, 30)
    email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
    email_field.send_keys(EMAIL)
    pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
    pass_field.send_keys(PASSWORD)
    pass_field.send_keys(Keys.RETURN)
    time.sleep(5)
    browser.get('https://www.facebook.com/search/posts/?q='+ text) # once logged in, free to open up any target page
    time.sleep(5)

    #scroll down
    #increase the range to sroll more
    #example: range(0,10) scrolls down 650+ images
    for j in range(0,3):
        print('Scrolling: ',j)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    time.sleep(5)

    soup=BeautifulSoup(browser.page_source,"html.parser")
    posts=soup.find_all("div",{"class":"du4w35lb l9j0dhe7"})
    
    time_stamp = datetime.today().strftime("%d_%m_%Y-%H_%M_%S")

    path = str(time_stamp)+'-'+ text +'-'+user+".csv"

    # Extracting Links from Posts
    linklist=[]
    pathlist=[]
    for post in posts:
        links=post.find_all('a')
        tmplnklst=[]
        for link in links:
            tmplnklst.append(link.attrs['href'])
        linklist.append(tmplnklst)
        pathlist.append(path)
    postlist=[]
    # Extracting text from post
    for post in posts:
        try:
            txt=post.find('div',{'class':'kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q'}).text
        except:
            txt="No Caption!"
        postlist.append(txt)
    
    Imagelist=[]
    for post in posts:
        imagelink=[]
        img = post.find('img')
        if img is not None:
            imagelink.append(img['src'])
        print(imagelink)
        Imagelist.append(imagelink)
        print(img)

    dct={'Post':postlist, 'img_link':Imagelist, 'Links':linklist, 'file_path':pathlist}
    df=pd.DataFrame(dct)
    
    
    print(time_stamp)
    df.to_csv(r"C:/Users/Administrator/Documents/social_media_django_2.0/project/facebook_csv/"+str(time_stamp)+'-'+ text +'-'+user+".csv", index=False)
    
    print(time_stamp)
    try:
        all_photo=soup.find_all("img")
        image_name= text
        if not os.path.exists('scrape_image/'+image_name):
            os.makedirs('scrape_image/'+image_name,mode = 0o777)

        #print(all_photo)
        i=0
        for photo in all_photo:
            i+=1
            link = photo['src']
            #Name=f'scrape_image/{image_name}/{image_name} {i}.jpg'
            Name=f'scrape_image/{image_name}/{image_name} {i}.jpg'
            #print((image_name+{i}).format(i))
            
            with open(Name, 'wb') as f:
                try:
                    img = requests.get(link)
                    f.write(img.content)
                    #print(os.path.getsize(Name))
                except:
                    continue
        # size=os.path.getsize(Name)
        # desired=2400
        # if size<desired:
        #     print(Name)
        #     os.remove(Name)
    except:
        pass

    return df


def Facebook_Photo(name):
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
        print(EMAIL)
        print(PASSWORD)
    

    #print(PASSWORD)
        
    browser = webdriver.Chrome(executable_path=r"C:\Users\Administrator\Documents\social_media_django_2.0\API\chromedriver.exe", options=options)
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
    browser.quit()
   
    all_photo=soup.find_all("img")
    image_name= text
    if not os.path.exists('scrape_image/'+image_name):
        os.makedirs('scrape_image/'+image_name,mode = 0o777)

    #print(all_photo)
    i=0
    for photo in all_photo:
        i+=1
        link = photo['src']
        #Name=f'scrape_image/{image_name}/{image_name} {i}.jpg'
        Name=f'scrape_image/{image_name}/{image_name} {i}.jpg'
        #print((image_name+{i}).format(i))
        
        
        with open(Name, 'wb') as f:
            try:
                img = requests.get(link)
                f.write(img.content)
                #print(os.path.getsize(Name))

            except:
                continue
            size=os.path.getsize(Name)
            desired=2400
            if size<desired:
                print(Name)
                os.remove(Name)

    return '200'


if __name__ == "__main__":
#     Google("covid","partho")
#     Twitter(500,"covid-19","partho")
     YouTube("pushpa","partho")
#     Facebook("Shaon.ComputerGeek","partho")
#     Facebook_Posts("opus technology limited","partho")
#     Facebook_Photo("opus technology limited")
