# -*- coding: utf-8 -*-
"""
Created on Thus March 10 21:20:43 2016

@author: Humber

** Read first: 
    Befor doing anything follow the steps - 
    Step 1:
        Before running the code save all the SUPC numbers in a single xlsx file 
        named - supc_data.xlsx, in the first sheet with the same heading and 
        remove the blank rows.
    Step 2:
        The output will be saved inside the success.txt and fail.txt files automatically
    Step 3:
        The process will stop cause of server block or by excaption. Follow the steps - 
            a. Make a copy of success.txt and fail.txt files
            b. Copy all the data from the files to their copies.
            c. The right side Console shows the last process as success or fail so you will get
            last supc code from thoes files for success of fail. Copy it.
            d. Find the supc code in the supc_data.xlsx file and delete that row and the
            above rows till the heading. Do not delete the heading.
            e. Before running close the right side Console and reopen it from the menu as 
            "Consoles -> Open an IPython console". Then rerun thee process again. 
            New links will be scrapped inside the success or fail text files.
            f. repeat from step b to e.

"""

import xlrd
import os.path
import urllib.request as req
import contextlib

supcXlsxFilePath = r'supc_data.xlsx'
successFile = r"success.txt"
failFile = r"fail.txt"
isProduct = '<div class="product-tuple-image">'
website = 'http://www.snapdeal.com/search?keyword='

def Serach_Snap_Deal(data):
    try:
        for supc in data:        
            supc = str(supc)
            supc = supc.replace("'","")
            supc = supc.replace("[","")
            supc = supc.replace("]","")
            
            url = website + supc
            
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            reqest = req.Request(url, headers = headers)            
            
            with contextlib.closing(req.urlopen(reqest)) as x:        
                matter = x.read().decode('UTF-8')    
                if (isProduct in matter):
                    with open(os.path.join(os.path.dirname(__file__), successFile), "a") as myfile:
                                myfile.write(website + supc + "\n")
                    print("success")
                else:                    
                    with open(os.path.join(os.path.dirname(__file__), failFile), "a") as myfile:
                                myfile.write(website + supc + "\n")
                    print("fail")
    except Exception as e:
        print("Exception from Serach_Snap_Deal method - " + str(e))


book = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), supcXlsxFilePath))
sheet = book.sheet_by_index(0) #or by the index it has in excel's sheet collection
 
data = [] #make a data store
for i in range(sheet.nrows):
    data.append(sheet.row_values(i))

data.pop(0) 
Serach_Snap_Deal(data)
