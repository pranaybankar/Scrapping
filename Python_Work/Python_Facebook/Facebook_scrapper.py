# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 06:30:23 2015

@author: Humber
"""



import requests
import http.cookiejar
from bs4 import BeautifulSoup

username = "username"
password = "password"
url = "https://www.facebook.com/"

headers = {'Host':'www.facebook.com',
'Origin':'http://www.facebook.com',
'Referer':'http://www.facebook.com/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11'}


s = requests.session()
print("session created")


login_data = {
    'locale':'en_US',
    'non_com_login':'',
    'email':username,
    'pass':password,
    'lsd':'20TOl'
    }

#jar = http.cookiejar.CookieJar()

request=s.post(url=url, data=login_data, verify=True)

print("page opened.")

html = request.content

soup = BeautifulSoup(html, "lxml")
print(soup.prettify())
#print (html)
#print (request.status_code)