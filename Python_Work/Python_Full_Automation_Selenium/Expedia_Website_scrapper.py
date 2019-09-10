# -*- coding: utf-8 -*-
"""
Created on Sat April 2 10:30:23 2016

@author: Humber-PC
"""
"""
Note- 
    1. As you run the script the link will open in a browser depending the webdriver used (I used chrome). 
    2. It will automatically start the scrapping process and the console will show the -
	"Save to MongoDB. Collection name - logiciqDB | document name - sitedata" output.
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
import time
import datetime
import sys, os 
import re

""" variable declaration"""
url = "https://www.expedia.co.in/New-York-Hotels-Row-NYC.h25033.Hotel-Information"
Hotel_Name = ''
Hotel_Rating = ''
Rate_details = ''
Date_of_stay = ''
Reviews = ''
Change_TimeStamp ='NON'
dates = ['21/05/2016','22/05/2016','23/05/2016','24/05/2016','25/05/2016'] #dates to be searched for
rates = []

try:
    
    """create driver"""
    driver = webdriver.Chrome()
    driver.get(url)    
    
    """Create a mongo client"""    
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logiciqDB
    
    """Save data to MongoDB"""
    def save_to_Mongo(Hotel_Name,Date_of_stay,Hotel_Rating,Rate_details,Reviews,TimeOfDay,Change_TimeStamp):
        try:        
            db.sitedata.insert_one({"Hotel_Name":Hotel_Name,"Date_of_stay":Date_of_stay,"Hotel_Rating":Hotel_Rating,"Rate_details":Rate_details,"Reviews":Reviews,"TimeOfDay":TimeOfDay,"Change_TimeStamp":Change_TimeStamp})
            print('Save to MongoDB. Collection name - logiciqDB | document name - sitedata')
        except Exception as e:
            print("Try block exception- " + str(e))

    """Get the HTML text using regex. The .text is not callable so I used regex"""
    def striphtml(data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)


    """ If the page load is taking time please increase the delay."""
    time.sleep(2)
    
    closePop = driver.find_element_by_css_selector('#modalCloseButton')    
    closePop.click()
    
    for x in dates:
        
        Date_of_stay = x      
                        
        Hotel_Name = str(driver.find_element_by_id('hotel-name').text)
        
        Hotel_Ratings = str(driver.find_element_by_class_name('guest-rating').text)
        Hotel_Rating = ' '.join(Hotel_Ratings.split())
                
        """ If the page load is taking time please increase the delay."""
        time.sleep(2)
        
        Date_of_checkIn = driver.find_element_by_xpath('//*[@id="availability-check-in"]')
        Date_of_checkIn.clear()
        Date_of_checkIn.send_keys(Date_of_stay)
        Date_of_checkIn = driver.find_element_by_xpath('//*[@id="availability-check-out"]')
        Date_of_checkIn.click() 
        
        check_availability = driver.find_element_by_css_selector('#update-availability-button')        
        check_availability.click()

        """ If the page load is taking time please increase the delay."""
        time.sleep(5)
#        
        """For room name and rates, the data is saved as Room name := Room rate seperated by pole (|)"""
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        table = soup.find('table')        
        tbodies = table.findAll('tbody')
        for tbody in tbodies:            
            tr = tbody.find('tr',attrs={'class':'rate-plan rate-plan-first '})
            
            """Get the room names"""
            td1 = tr.find('td',attrs={'class':'room-info'})                           
            h3 = td1.find('h3')
            room = striphtml(str(h3))
                        
            """Get the room rates"""
            td2 = tr.find('td',attrs={'class':'avg-rate'})
            rateN = td2.find('span',attrs={"class":" room-price one-night-room-price "})            
            if rateN == None:
                rate = 'Sold Out'
                
            else:
                rate = striphtml(str(rateN)) 
            
            rates.append(room + ' := ' + rate)
        
        Rate_details = '|'.join(rates)
                
        """ If the page load is taking time please increase the delay."""
        time.sleep(5)    
        
        """This will help to automatically go to reviews"""
        RevLink = driver.find_element_by_css_selector('body > div.site-content-wrap.hotelInformation > div.site-content.cols-row > section > section > div.summary-wrapper > article > div > div.cols-nested > a')                
        RevLink.click()
        
        """ If the page load is taking time please increase the delay."""
        time.sleep(5)    
        
        """for now I'm taking only one review as the huge  data will be confusing for the POC. 
        I'm working on the looping and saving of all the data which will be update in the next version."""        
        Reviewss = str(driver.find_element_by_css_selector('#reviews > article:nth-child(1) > div.details').text)
        Reviews = ' '.join(Reviewss.split())
        
        """Current timestamp"""
        TimeOfDay = datetime.datetime.now()
                
        """Data change logic"""
        DateOfStay = db.sitedate.find_one({"Date_of_stay": Date_of_stay})   
        if DateOfStay is None:        # check data availability
            save_to_Mongo(Hotel_Name,Date_of_stay,Hotel_Rating,Rate_details,Reviews,TimeOfDay,Change_TimeStamp)
        else:
            #if the newer and older "Rate_details" matches then the "Change_TimeStamp" will get updated else
            #save it as NON
            body = db.sitedate.find_one({"Date_of_stay": Date_of_stay}).sort({"TimeOfDay": 1 }) 
            original = body["Rate_details"]
            newer = Rate_details
            if original == newer:
                Change_TimeStamp = datetime.datetime.utcnow()
                save_to_Mongo(Hotel_Name,Date_of_stay,Hotel_Rating,Rate_details,Reviews,TimeOfDay,Change_TimeStamp)
            else:
                save_to_Mongo(Hotel_Name,Date_of_stay,Hotel_Rating,Rate_details,Reviews,TimeOfDay,Change_TimeStamp)
        
    driver.quit()
         
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('Exception type - '+ str(exc_type),' | Exception? - '+ str(e) ,' | Line # - '+ str(exc_tb.tb_lineno))
    