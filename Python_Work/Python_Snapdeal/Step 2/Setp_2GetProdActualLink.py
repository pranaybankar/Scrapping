# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 18:49:10 2016

@author: Humber
** Read first: 
    Befor doing anything follow the steps - 
    Step 1:
        Before running the code save all the Links from step 1 in a single xlsx file 
        named - getProdData.xlsx, in the first sheet and remove the blank rows.
    Step 2:
        The output will be saved inside the success.txt file automatically.
    Step 3:
        The process will stop cause of server block or by excaption. Follow the steps - 
            a. Make a copy of success.txt file.
            b. Copy all the data from the file to its copy.
            c. The right side Console shows the last process a success or fail so you will
            last supc number from thoes files where the img link will have that supc number. 
            Copy it.
            d. Find the supc code in the getProdData.xlsx file and delete that row and the
            above rows.
            e. Before running close the right side Console and reopen it from the menu as 
            "Consoles -> Open an IPython console". Then rerun thee process again. 
            New links will be scrapped inside the success or fail text files.
            f. repeat from step b to e.
"""
import xlrd
import os.path
from bs4 import BeautifulSoup
import urllib.request as req
import contextlib

productUrlXlsxFilePath = r'Input_2getProdData.xlsx'
prodcutLinkFile = r"Output_2prodLinks.txt"
failProdcutLinkFile = r"failProdLinks.txt"
isProduct = r'<div class="product-tuple-image">'

"""Delete temp output file"""
try:
    with open(os.path.join(os.path.dirname(__file__), prodcutLinkFile)) as existing_file:
        existing_file.close()
        os.remove(os.path.join(os.path.dirname(__file__), prodcutLinkFile))
except Exception as e:
    print("Delete Output_2prodLinks.txt file exception- " + str(e))

def get_Prod_Url(data):
    try:
        for productUrl in data:        
            productUrl = str(productUrl)
            productUrl = productUrl.replace("'","").replace("[","").replace("]","")
            
            """Get SUPC Code"""    
            supcCode = productUrl.split("keyword=",1)[1]
            
            """Here we are knowcking the door of snapdeal server as a human agent and not python"""
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            reqest = req.Request(productUrl, headers = headers) 
            
            with contextlib.closing(req.urlopen(reqest)) as url: 
                content = url.read().decode('UTF-8') 
                soup = BeautifulSoup(content,"lxml")
                
                div = soup.find('div',attrs={"class":"product-tuple-image"})
                link = div.find('a')['href']                 
                                
                with open(os.path.join(os.path.dirname(__file__), prodcutLinkFile), "a") as myfile:
                    myfile.write(str(link) +','+ str(supcCode) + "\n")
                    print("step 2 - success")
                

    except Exception as e:
        if "500" in str(e):
            print("Server block. The exception Value stackTrace - " + str(e))
        else:    
            print("The URL does not have product as it's a FAIL URL. Please provide next URL. The exception Value stackTrace - " + str(e))

book = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), productUrlXlsxFilePath))
sheet = book.sheet_by_index(0) #or by the index it has in excel's sheet collection
 
data = [] #make a data store
for i in range(sheet.nrows):
    data.append(sheet.row_values(i))
    
get_Prod_Url(data)

