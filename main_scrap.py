from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import random as rd
import time
import pandas as pd
import re
import pandas as pd


def wait(duration='short'):
    if duration =='short':
        return time.sleep(rd.randrange(1,3))
    elif duration =='medium':
        return time.sleep(rd.randrange(3,6))
    elif duration =='long':
        return time.sleep(rd.randrange(9,12))


username = '' #tulis username twitter disini

password = '' #tulis password twitter disini

# Proxy settings

# http://free-proxy.cz/en/proxylist/country/SG/all/ping/all
proxy_ip = '20.24.43.214'
proxy_port = '8123'

# Set up proxy configuration for Chrome WebDriver
proxy_options = {
    'proxy': {
        'httpProxy': f'{proxy_ip}:{proxy_port}',
        'ftpProxy': f'{proxy_ip}:{proxy_port}',
        'sslProxy': f'{proxy_ip}:{proxy_port}',
        'proxyType': 'MANUAL',
    }
}

# Set up Chrome WebDriver with proxy options
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe", options=webdriver.ChromeOptions().add_experimental_option('proxy', proxy_options))

driver.get(f'https://www.twitter.com')

wait('medium')

#find
username_field = driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
login_selanjutnya_button = driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')

#do login
username_field.send_keys(username)
wait()
login_selanjutnya_button.click()
wait()
password_field = driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
masuk_button = driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
wait()
password_field.send_keys(password)
masuk_button.click()
wait('medium')


date = pd.read_csv("tanggal_2022_edit.csv",sep=";")

since_list = date["since"].to_list()
until_list = date["until"].to_list()

swr = 0

for i in range(len(since_list)):
        
    #choose the date
    until = until_list[i]
    since = since_list[i]

    #query
    search_query = f'("Global Warming" OR "Climate Change") lang:id until:{until} since:{since}'
    #scraptime
    scraptime = 200

    #path
    driver.get(f'https://twitter.com/search?q=%22climate%20change%22%20OR%20%22perubahan%20iklim%22%20lang%3Aid%20since%3A{since}%20until%3A{until}&src=typed_query&f=live')
    wait()
    pyautogui.moveTo(383, 442)

    start_time = time.time()
    all_tweets = []
    verify_tweet_list = []
    time.sleep(1)
    
    end_count = 0
    

    while time.time() < start_time + scraptime:
        try:
            users = driver.find_elements(By.XPATH,"//*[@class='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu']/div[1]")
            tweets = driver.find_elements(By.XPATH,"//*[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']")
            tweet_list = [tweet.text for tweet in tweets]
            users_list = [user.text for user in users]
            if tweet_list != verify_tweet_list:
                end_count = 0
                for user,tweet in zip(users_list,tweet_list):
                    split_data = user.split('\n')
                    accountname = split_data[0]
                    username = split_data[1]
                    date = split_data[3]

                    tweet = re.sub(r"\n", " ", tweet)

                    all_tweets.append({'accountname':accountname,'username':username,'tweet': tweet,'date':date})
            verify_tweet_list = tweet_list
            pyautogui.scroll(-1500)
            time.sleep(0.3)
            pyautogui.scroll(-1000)
            time.sleep(1)
            if tweet_list == verify_tweet_list:
                if end_count == 15:
                    break
                end_count = end_count + 1
        except:
            pyautogui.scroll(-1500)
            time.sleep(0.3)
            pyautogui.scroll(-1000)
            time.sleep(1)
            continue
    if all_tweets != []:
        swr = 0 
        df_tweets = pd.DataFrame(all_tweets)
        output_filename = f'tweets_climate_change_id_{since}_{until}.csv'
        df_tweets.to_csv(output_filename, index=False)
        print(f"Data saved to {output_filename} , length:{len(all_tweets)}")
    elif all_tweets == []:
        if swr > 4:
            driver.quit()
            break 
        swr = swr + 1


        
    
    # Close the browser
driver.quit()


