# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 07:31:10 2015

@author: Humber
"""
#Include the lib, define some var
import http.cookiejar, urllib.request

# variable declaration
username = "username"
password = "password"
url = "https://www.facebook.com/login.php"

#send POST request
login_data = urllib.parse.urlencode    \
({                               \
    'locale':'en_US',       \
    'email' : username,       \
    'pass' : password,      \
    'login_node' : '0',        \
    'cookietime' : '315360000'         \    
}).encode("utf-8")

request = urllib.request.urlopen(url, data=login_data)
print("page opened.")
print(request)