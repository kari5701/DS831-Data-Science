# ***  Group 13 (Simon, Melek, Karina and Flemming)  ***
# ***  Preliminary hand-in of assignment 1 of 3  ***

import urllib
import time
from bs4 import BeautifulSoup
import random
import os
import pandas as pd

# ************  Below we download the pages containing yearly overviews  *****

print()
print('Welcome to a deep dive into civil aviation accidents!')

begin_year = int(input('Earliest year you want to scrape (1819 or later): '))
end_year   = int(input('Last year you want to scrape: '))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "utf-8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0"
} 


for i in range(end_year,begin_year-1,-1):
    url = 'https://en.wikipedia.org/wiki/Category:Aviation_accidents_and_incidents_in_'+str(i)
    try:
        request = urllib.request.Request( url, None, headers )
        response = urllib.request.urlopen( request )
        with open('data03/accidents_in_'+str(i)+'.html', 'w',encoding="utf-8") as f:
            f.write(str(response.read().decode('utf-8')))
        time.sleep(1+random.randint(0,100)/50)
        print('Did '+str(i))
    except urllib.error.HTTPError:
        print("Page with ID "+str(id)+" found")

# *****  Below we extract roughly the relevant hrefs from yearly overviews ****

to_parse = os.listdir("data03")

column_headers = ['local_file','year','link-in-year','acciname',
                  'accihref', 'GR13_comment']
acci_df = pd.DataFrame(columns = column_headers)

for year_overview in to_parse:
    
    year_int = int(year_overview[13:17])
    
    parsefile1 = open('data03/'+year_overview,encoding="utf-8").read()
    
    if '<h3>0–9</h3>' in parsefile1:
        splitter1 = '<h3>0–9</h3>'
    elif '<h3>A</h3>' in parsefile1:
        splitter1 = '<h3>A</h3>'
    elif '<h3>B</h3>' in parsefile1:
        splitter1 = '<h3>B</h3>'
    elif '<h3>C</h3>' in parsefile1:
        splitter1 = '<h3>C</h3>'
    elif '<h3>C</h3>' in parsefile1:
        splitter1 = '<h3>V</h3>'
    else:
        splitter1 = '<p>This category'
    
    parsefile2 = parsefile1.split(splitter1)[1]
    
    parsefile3 = parsefile2.split('!--esi')[0]
    
    doc = BeautifulSoup(parsefile3, "html.parser")
        
    tag = doc.find_all('a')
    
    for i in range(len(tag)):
        current_row = len(acci_df.index)
        acci_df.loc[current_row,['local_file']]= str(year_int)+'--'+str(i+1)+'.html' 
        acci_df.loc[current_row,['year']]= year_int
        acci_df.loc[current_row,['link-in-year']] = i+1
        acci_df.loc[current_row,['acciname']]=  tag[i].text
        acci_df.loc[current_row,['accihref']]= tag[i]['href']
        acci_df.loc[current_row,['GR13_comment']]= 'for now, no comments'
    print('Finished work on overview: ',year_overview)

# ************  Below we download the pages for the individual accidents  *****

print()
print('***  Now we will scrape wiki-pages accidentr by accidents  ***')
print()

for i in range(len(acci_df)):

    url = 'https://en.wikipedia.org'+acci_df.loc[i, ['accihref']].values[0]
    # gem_den = url
    try:
        request = urllib.request.Request( url, None, headers )
        response = urllib.request.urlopen( request )
        with open('data03detailed/'+str(acci_df.loc[i, ['year']].values[0])+'--'+str(acci_df.loc[i, ['link-in-year']].values[0])+'.html', 'w',encoding="utf-8") as f:
            f.write(str(response.read().decode('utf-8')))
        time.sleep(1+random.randint(0,100)/100)
        # print('Did '+str(acci_df[i]['year'])+'--'+str(acci_df[i]['link-in-year']))
    except urllib.error.HTTPError:
        print("Page with ID - to be updated - found")
        
acci_df.to_csv('output_ass1.csv')        
