#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:28:31 2023

@author: simonnordby
"""
import re
import urllib
import time
import unicodedata

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

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

# An empty list to append to later. 
data = []

# Function to get keys from the infobox. Used later.
# We replace nonbreaking space with space (aircraft type). \xa0 is a non-breaking space in unicode.
def get_infobox_value(soup, name, raise_error=False):
    for key in soup.find_all("th", {"class":"infobox-label"}):
        key_name = key.text.lower().replace("\xa0", " ")
        if name.lower() in key.text.lower() or name.lower() in key_name: 
            data = key.find_next_sibling("td")
            return data
        
    return None

# Define a function to extract the first number using regular expression.
def extract_first_number(text):
    match = re.search(r'\b\d+\b', str(text))  # Match the first number in the text
    return int(match.group()) if match else None  # Return the matched number if found, else None

# Iterating through the base-url, finding years with accidents in.
for year in range(1819, 2024):
    url = 'https://en.wikipedia.org/wiki/Category:Aviation_accidents_and_incidents_in_'+str(year)
    try:
        # time.sleep(0.1)
        request = urllib.request.Request(url,None,headers)
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response.read().decode('utf-8'),"html.parser")
        print('Working through '+str(year))
        
        # Narrow down the area in the html files.
        category_links = soup.find("div", {"id":"mw-pages"}) 
        
        # If there is no accident-links in the url print and stop. 
        if not category_links: 
            print('No links for accidents in: ' + str(year))
        else:
            
            # Finding all links(a) in the area.
            crash_in_year = category_links.find_all("a",)
            
            # List comprehention
            crash_links = [ 
            link.get("href")
            for link in crash_in_year
                ]
            
            # We go a step deeper. Iterating through every link for individual accidents, searching for infoboxes. 
            for link in crash_links: 
                url = "https://en.wikipedia.org" + link   
                request = urllib.request.Request(url,None,headers)
                response = urllib.request.urlopen(request)
                soup = BeautifulSoup(response.read().decode('utf-8'),"html.parser")
                infobox = soup.find("table", {"class":"infobox"}) 
                
                # Finding infoboxes in individual accidents.
                if not infobox: 
                    print("No infobox found")
                else:
                    
                    # Check if 'Date' information is present before extracting other values
                    date_value = get_infobox_value(infobox, "Date")
                    if date_value:
                          
                        # A dict with the keys and values. The values are extracted with the function.
                        info_values = { 
                                        "Date": get_infobox_value(infobox, "Date"),
                                       "Summary": get_infobox_value(infobox, "Summary"),
                                       "Site": get_infobox_value(infobox, "Site"), # We use site and extract coordinates and location from it later 
                                       "Aircraft type": get_infobox_value(infobox, "Aircraft type"),
                                       "Operator": get_infobox_value(infobox, "Operator"),
                                       "Passengers": get_infobox_value(infobox, "Passengers"),
                                       "Crew": get_infobox_value(infobox, "Crew"),
                                       "Fatalities": get_infobox_value(infobox, "Fatalities"),
                                       "Injuries": get_infobox_value(infobox, "Injuries"),
                                       "Survivors": get_infobox_value(infobox, "Survivors"),
                                       }

                        # Extracting data about location and coordinates from Site.
                        site = info_values.get('Site')
                        if site:
                            info_values['Location'] = site.select_one('td.infobox-data > a') 
                            info_values['Coordinates'] = site.find('span', {'class': 'geo'})
    
                        # Name of accident
                        info_values['Name'] = soup.find("caption", {"class":"infobox-title fn org summary"})                     
                        
                        # Cleaing up the data. If there is a value for each key, get the textual content of the HTML-code.
                        for k, v in info_values.items():  
                            if v: 
                                info_values[k] = unicodedata.normalize('NFKD', v.get_text())
                       
                        # Year of accident
                        info_values['Year'] = year 
                        
                        # Divide coordinates up in columns for latitude and longitude
                        coordinates = info_values.get('Coordinates')
                        if coordinates:
                            info_values['Latitude'] = info_values['Coordinates'].split(';')[0].strip() # Removes white space
                            info_values['Longitude'] = info_values['Coordinates'].split(';')[1].strip()
                        
                        info_values['Link'] = url
                        
                        
                        data.append(info_values)
                        
    # Except if there is no page from the year.
    except urllib.error.HTTPError:
        print('Page from year ' + str(year) + ' not found ')

# Set up the dataframe and export it as a csv-file.
df = pd.DataFrame(data)

            ################## Cleaning the Dataframe ##################
# # Drop empty rows
# df.dropna(how='all', inplace=True)

# Clean columns with only numbers - remove special characters
columns_to_clean = ['Passengers', 'Crew', 'Survivors', 'Fatalities', 'Injuries']
for column in columns_to_clean:
    df[column] = df[column].apply(extract_first_number)

# Insert new columns in df - On board, Death Rate and Injury Rate.
df['Onboard'] = (df['Passengers'].fillna(0) + df['Crew'].fillna(0))

# Use np.NAN for missing values in death_rate and injury_rate
df['Death Rate'] = df.apply(lambda row: 
                     row['Fatalities'] / row['Onboard'] if 
                     (row['Onboard'] != 0 and 
                      not pd.isnull(row['Fatalities'])) 
                     else np.NAN, 
                     axis=1)

df['Injury Rate'] = df.apply(lambda row: 
                     row['Injuries'] / row['Onboard'] if 
                     (row['Onboard'] != 0 and 
                      not pd.isnull(row['Injuries']))  
                     else np.NAN, 
                     axis=1)
    
# Function to get get coordinates from location using a geocoder
def get_lat_lon(location_name):
    
    # Initialize the Nominatim geocoder
    geolocator = Nominatim(user_agent="my_geocoder")
    result = [False, None, None]  # Represents: found it, latitude, tongitude
    try:
        # Geocode the location
        location = geolocator.geocode(location_name)
        if location:
            result[0] = True
            result[1] = location.latitude
            result[2] = location.longitude
        else:
            print(f"Could not find coordinates for {location_name}")
    except Exception as e:
        print(f"Error: {e}")
    return result
    
# Function to get coordinates for missing locations in the DataFrame
def update_coordinates(row):
    location = row['Location']
    if pd.notnull(location) and (pd.isnull(row['Latitude']) or pd.isnull(row['Longitude'])):
        result = get_lat_lon(location)
        if result[0]:
            return pd.Series({'Latitude': result[1], 'Longitude': result[2]})
        else:
            return pd.Series({'Latitude': None, 'Longitude': None})
    else:
        return pd.Series({'Latitude': row['Latitude'], 'Longitude': row['Longitude']})

# Apply the function to update missing coordinates in the DataFrame
df[['Latitude', 'Longitude']] = df.apply(update_coordinates, axis=1)

# Remove site and coordinates, as they are redundant
del df['Coordinates']
del df['Site']

df.to_csv('aviation_accidents.csv', index=False, encoding='utf-8')

