from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# other necessary ones
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re
import datetime
import requests

def Facebook_Posts(name):
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

    print(df)

    df.to_csv("Facebook_post.csv", index=False)

    all_photo=soup.find_all("img")
    image_name= text

    #print(all_photo)
    i=0
    for photo in all_photo:
        i+=1
        link = photo['src']
        Name=f'{image_name} {i}.jpg'
        #print((image_name+{i}).format(i))
        
        with open(Name, 'wb') as f:
            try:
                img = requests.get(link)
                f.write(img.content)
            except:
                continue

Facebook_Posts("opus technology limited")