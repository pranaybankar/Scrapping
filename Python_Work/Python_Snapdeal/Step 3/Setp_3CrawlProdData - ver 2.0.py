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
import re


crawlProdData = r'Input_3crawlProdData.xlsx'
allData = r"Output_3AllData.txt"
imgList = []
breadcrumData = ''

"""Delete temp output file"""
try:
    with open(os.path.join(os.path.dirname(__file__), allData)) as existing_file:
        existing_file.close()
        os.remove(os.path.join(os.path.dirname(__file__), allData))
except Exception as e:
    print("Delete Output_3AllData.txt file exception- " + str(e))

def save_to_file(supcCode,productUrl,breadCrum,img,title,uli,matter):
    try:   
        with open(os.path.join(os.path.dirname(__file__), allData), "a") as myfile:
            myfile.write(str(supcCode) +','+ str(productUrl) +','+ str(breadCrum) +','+ str(img) +','+ title +','+ uli +','+ matter +'\n')
            print("step 3 - success")
    except Exception as e:
        print("save_to_file method exception- " + str(e))
        
def get_Prod_Data(data):
    try:
#        productUrl = r"http://www.snapdeal.com/product/total-gym-home-gym-adjustable/683563847221#bcrumbSearch:SDL717687292"
#        productUrl = r"http://www.snapdeal.com/product/jaspo-kids-delite-pro-junior/662812944654#bcrumbSearch:SDL218198354"
         
        for productUrl in data:        
            productUrl = str(productUrl)

            productUrl = productUrl.replace("'","").replace("[","").replace("]","")
            
         
        
            """Here we are knowcking the door of snapdeal server as a human agent and not python"""
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            reqest = req.Request(productUrl, headers = headers) 
        
            with contextlib.closing(req.urlopen(reqest)) as url: 
                content = url.read().decode('UTF-8') 
                soup = BeautifulSoup(content,"lxml")
                
                """Get Bread Crums / Category"""
                breadCrumsss = soup.find('div',attrs={"id":"breadCrumbWrapper2"})
                breadCrumsss.findAll('span')
                breadCrums = breadCrumsss.text
                breadCrum = ' '.join(breadCrums.split()).replace(',','--').replace('Sports & Fitness Fitness Fitness Equipment','Sports & Fitness > Fitness > Fitness Equipment >')
                               
                     
                """Get image link"""    
                
                imgsss = soup.find('div',attrs={"id":"bx-pager-left-image-panel"}) 
                
                imgss = imgsss.findAll('img')
                
                for imgs in imgss:                                
                    imgList.append(str(imgs))
                    
                rr = '||'.join(imgList)
                
    #            img = re.findall('http://n1.sdlcdn.com/imgs\/[a-z]\/[0-9]\/[a-z]\/[\-a-zA-Z0-9]+.jpg', rr)
                
                
                
                """Get product title"""    
                titless = soup.find('h1',attrs={"class":"pdp-e-i-head"})        
                titles = titless.text
                title = titles.replace(',','--')
                
                """Get product Highlights"""    
                div = soup.find('div',attrs={"class":"spec-body"})        
                uls = div.find('ul',attrs={"class":"dtls-list clear"})        
                ul = uls.text
                uli = ' '.join(ul.split()).replace(',','--')       
                
                """Get SUPC Code"""    
                supcCode = uli.split("SUPC: ",1)[1]
                
                """Get product Details"""    
                div1 = soup.find('div',attrs={"class":"detailssubbox"})                        
                matters = div1.text
                matter = ' '.join(matters.split()).replace(',','--')
                
                save_to_file(supcCode,productUrl,breadCrum,rr,title,uli,matter)
                
                imgList.clear()
                
    except Exception as e:
        print("get_Prod_Data method exception- " + str(e))

"""Start of the Program"""
book = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), crawlProdData))
sheet = book.sheet_by_index(0) #or by the index it has in excel's sheet collection
 
data = [] #make a data store
for i in range(sheet.nrows):
    data.append(sheet.row_values(i))
    
get_Prod_Data(data)

