# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 12:56:17 2017

@author: Humber
Description: 
    First of all, thanks for giving this opportunity!!
    I tried to make the code as simple as possible. I covered only the main data points for scrapping.
    The code is not object oriented (no class and objects), it’s a simple interpretation.
    I never tried classes, scrapy in python so at this stage they are missing but yes the code can be improvised.
    I'm familiar with urllib, BeautifulSoup so used them for request and parsing data.
    The data is in the 'Output_Dubizzle_books_AllData.csv' file under same folder.
    
    Thank you again for this test.
"""

import os.path
import urllib.request as req
import contextlib
from bs4 import BeautifulSoup
from dateutil.parser import parse
import datetime
import os ,sys


"""variable defination"""
mainUrl = 'https://uae.dubizzle.com/classified/books/'
allData = r"Output_Dubizzle_books_AllData.csv"

"""visit website as a User agent and not as a bot."""
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
reqest = req.Request(mainUrl, headers = headers)  


"""Delete temp output file"""
try:
    with open(os.path.join(os.path.dirname(__file__), allData)) as existing_file:
        existing_file.close()
        os.remove(os.path.join(os.path.dirname(__file__), allData))
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('Exception type - '+ str(exc_type),' | Exception? - '+ str(e) ,' | Line # - '+ str(exc_tb.tb_lineno))

"""writing the hearder row to the csv file"""
try:   
    with open(os.path.join(os.path.dirname(__file__), allData), "a") as myfile:
        myfile.write('listing_id,title,title_url,price,dates,age,usage,condition'+'\n')        
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('Exception type - '+ str(exc_type),' | Exception? - '+ str(e) ,' | Line # - '+ str(exc_tb.tb_lineno))
    
"""Save to output file"""
def save_to_csv(title_url,title,listing_id,price,dates,age,usage,condition):
    try:   
        with open(os.path.join(os.path.dirname(__file__), allData), "a",encoding="utf-8") as myfile:
            myfile.write(str(listing_id)+','+ str(title) +','+ str(title_url) +','+ str(price) +','+ str(dates) +','+ str(age) +','+ str(usage) +','+ str(condition) +'\n')
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Exception type - '+ str(exc_type),' | Exception? - '+ str(e) ,' | Line # - '+ str(exc_tb.tb_lineno))
		
"""sarape data and save to csv"""
def parseData(soup):
    try:
        """find the outer html and pars to inner html i.e. list-item-wrapper class"""
        outerDiv = soup.find('div',attrs={"class":"show-highlighted-ads"})           
        for innerDiv in outerDiv.find_all('div', attrs={"class":"list-item-wrapper"}) :
            """Find title_url"""
            titles = innerDiv.find('h3',attrs={"id":"title"})
            title_url = titles.find('a')['href']    
            title_url = title_url.strip()
            
            """Find title"""
            title = titles.find('span',attrs={"class":"title"})
            title= title.text
            title= title.replace(",","|")
            title= title.strip()
            
            """Find listing id"""
            listing_id = innerDiv.find('div',attrs={"class":"listing-item"})['data-id']
            listing_id = listing_id.strip()
            
            """Find price of book"""
            price = innerDiv.find('div',attrs={"class":"price"})
            price = price.text
            price= price.replace(",","")
            price = price.strip()
            
            """Find listing date"""
            dates = innerDiv.find('p',attrs={"class":"date"})
            dates = dates.text
            dates = dates.strip()
            dates = parse(dates).date()   
            dates = str(dates)
            dates = datetime.datetime.strptime(dates, '%Y-%m-%d').strftime('%Y-%m-%d')
            
            """Find Age"""        
            ages = innerDiv.find('ul',attrs={"class":"features"})
            age = ages.find('li').findNext('strong')
            age = age.text
            age = age.strip()
            
            """Find usage"""        
            usage = innerDiv.find('ul',attrs={"class":"features"})
            usage = usage.findNext('li').findNext('li').findNext('strong')
            usage = usage.text
            usage = usage.strip()
            
            """Find usage"""        
            condition = innerDiv.find('ul',attrs={"class":"features"}).findNext('ul',attrs={"class":"features"})
            condition = condition.find('li').findNext('strong')
            condition = condition.text
            condition = condition.strip()
            
            """save to csv file"""        
            save_to_csv(title_url,title,listing_id,price,dates,age,usage,condition)
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Exception type - '+ str(exc_type),' | Exception? - '+ str(e) ,' | Line # - '+ str(exc_tb.tb_lineno))
		
"""Start of scrapper"""
try:
    with contextlib.closing(req.urlopen(reqest)) as url: 
        content = url.read().decode('UTF-8') 
        soup = BeautifulSoup(content,"lxml")
        
        """find last page no"""
        lastpage = soup.find('div',attrs={"class":"paging_forward"}).findNext('a',attrs={"id":"last_page"})['href']
        lastpage = lastpage.replace('/classified/books/?page=','')
        lastPageNo = int(lastpage)
        
        for i in range(1,lastPageNo+1):
            try:
                headers = {}
                headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
                mainUrll = mainUrl + '?page='+str(i)
                print(mainUrll)
                reqest = req.Request(mainUrll, headers = headers) 
                
                with contextlib.closing(req.urlopen(reqest)) as url: 
                    content = url.read().decode('UTF-8') 
                    soup = BeautifulSoup(content,"lxml")
                    
                    """pasre the data"""
                    parseData(soup)                    
                    
                    """Process persuation"""
                    print('Data saved to csv file from page '+str(i)+' !')
                    
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('Exception type - '+ str(exc_type),' | Exception? - '+ str(e) ,' | Line # - '+ str(exc_tb.tb_lineno))

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('Exception type - '+ str(exc_type),' | Exception? - '+ str(e) ,' | Line # - '+ str(exc_tb.tb_lineno))