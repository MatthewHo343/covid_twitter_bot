from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import tweepy

def main():
    # remove previous data to ensure no duplication

    folderDir = '/Users/focus/Desktop/Projects/covid_twitter_bot/data'
    if (len(os.listdir(folderDir)) == 1):
        os.remove('/Users/focus/Desktop/Projects/covid_twitter_bot/data/data.csv')
        print("data.csv removed")
        os.remove('/Users/focus/Desktop/Projects/covid_twitter_bot/plot.png')
        print("plot.png removed")
    fetch()
    visualize()
    tweet()


def fetch():

    URL = 'https://go.illinois.edu/COVIDTestingData'

    # Path to the chromedriver
    CPath = '/Users/focus/Desktop/Projects/covid_twitter_bot/chromedriver'
    # Preferences for the chrome driver to redirect downloads to folder
    prefs = {"download.default_directory" : "/Users/focus/Desktop/Projects/covid_twitter_bot/data"}
    
    # Sets chrome options given preferences
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs",prefs)

    # Creates webdriver and goes to desired link
    chrome = webdriver.Chrome(executable_path=CPath, options=chromeOptions)
    chrome.get(URL)

    # Sleeps to guarantee everything loads
    time.sleep(3)

    # Toggles element to display hidden button
    toggle = chrome.find_element_by_id('element3')
    chrome.execute_script("arguments[0].setAttribute('class','dashboard-element chart active')", toggle)

    # Click button that was previously hidden
    button = chrome.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[3]/div/div/div[2]/div/div[3]/div/a[1]')
    button.click()

    # Sleeps again to guarantee everything loads
    time.sleep(1)

    # Renames the file and downloads
    action1 = ActionChains(chrome)
    action1.send_keys(Keys.TAB)
    action1.send_keys(Keys.TAB)
    action1.send_keys('data')
    action1.send_keys(Keys.ENTER)
    action1.perform()

    # Sleeps again to guarantee everything loads
    time.sleep(3)

    # Closes the browser
    chrome.close()
    print("data.csv fetched")

# creates a data visualization of trends in the past 7 days of results
def visualize():
   
   # Load the data into pandas
    data = pd.read_csv('data/data.csv', encoding = 'utf-8').fillna(0)
   
    # narrows dataset to most recent entries
    latest = data.tail(7)
   
    # iterates through the dates to convert UNIX time to something legible
    # for i in range(len(latest)):
    #     boo = latest.loc([0],["New Cases"])
    #     print(boo)

    # creates the plot based on our modifications
    latest.plot(x = "_time", y = ["New Cases"])
    
    # saves the current figure 
    fig1 = plt.gcf()

    # show the figure
    plt.show(block=False)
    plt.pause(3)
    plt.close()

    # redraw the figure and save
    plt.draw()
    fig1.savefig('plot', dpi=100)
    print("complete visualization")

def tweet():
    # API details
    # omitted into auth_keys.txt for privacy reasons
    
    auth = tweepy.OAuthHandler(

            twitter_auth_keys['consumer_key'],

            twitter_auth_keys['consumer_secret']

            )

    auth.set_access_token(

            twitter_auth_keys['access_token'],

            twitter_auth_keys['access_token_secret']

            )
    api = tweepy.API(auth)
    tweet = "Hail to the Orange"

    api.update_status(status=tweet)
    print("tweeted")

main()