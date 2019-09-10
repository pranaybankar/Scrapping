# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 13:30:23 2015

@author: Humber
"""


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pickle
import time

# variable declaration
username = "username"
password = "password"
url = "https://www.facebook.com/"
pickle_file = 'D:\Facebok_scrape_data.pickle'
profileLink = "profileLink"
class_name = "fwb"
hour = "js_41"
tag = 'div'

#create driver
driver = webdriver.Firefox()
driver.get(url)

print("page loaded.")
# If the page load is taking time please increase the time. My internet takes 15 seconds.
time.sleep(15)

#provide login details and submit
inputEmail = driver.find_element_by_id("email")
inputEmail.send_keys(username)
inputPass = driver.find_element_by_id("pass")
inputPass.send_keys(password)
inputPass.submit()

print("Details submited.")

pname = (driver.find_element_by_tag_name(tag))

print(pname.text)

with open(pickle_file, 'wb') as handle:
  pickle.dump(pname.text, handle)
  
driver.quit()