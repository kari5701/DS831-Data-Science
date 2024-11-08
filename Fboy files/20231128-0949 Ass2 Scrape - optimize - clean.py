
import pandas as pd
from bs4 import BeautifulSoup
import time
from html import unescape
import numpy as np
from geopy.geocoders import Nominatim

accidetails = pd.read_csv('output_ass1.csv')
accidetails = accidetails.set_index('local_file')
accidetails['has_infobox'] = False
files = accidetails.index.tolist()

print(len(files))
time.sleep(1)

# Below all headings in all infoboxes fo right type in accident-pages are scraped,
# only ater unwanted headings=df.columns are deleted

for file in files:  
    text = open('data03detailed/'+file, encoding="utf-8").read()
    soup = BeautifulSoup(text,features="lxml")
    # first check if there is a info-box at all
    if 'infobox vcard vevent' in text:
        accidetails.loc[file, 'has_infobox'] = True
        table_cont = soup.find('table', attrs={'class': 'infobox vcard vevent'})
        all_trs = table_cont.find_all('tr')
    
        for tr in all_trs:
            th = tr.find('th', {'class': 'infobox-label'})
            td = tr.find('td', {'class': 'infobox-data'})
            
            if th and td:
                header_text = unescape(th.get_text(strip=True))
                data_text = unescape(td.get_text(strip=True))
                accidetails.loc[file, header_text] = data_text
                
    print('So by now I scraped up to: ',file)

# Drop rows that does not have infobox of the expected type:
accidetails = accidetails[accidetails['has_infobox']]
files = accidetails.index.tolist()

                
# ********** Following steps aim at geo-localizing more accidents ****************************                

eliminate = ['near','over','km from','north of','east of','south of','west of','I will add more']
for i in range(len(eliminate)):
    eliminate.append(eliminate[i].capitalize())    

loops_done = [0, 0, 0]

accidetails['latitude'] = np.nan
accidetails['longitude'] = np.nan

# it is not so well-structured bugt first we get this FUNCION stated then there are several loops,
# only the first loop below does NOT use the function

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

# First we try to split up Site hoping to find valid latitude
# and longitude in the last split sections:
# Note that in this part we do NOT use the get_lat_lon function above (but we do in the following sections)

for file in files:
    # not pd.isna checks that the folllowing items contains something else than "empty" (nan)
    if not pd.isna(accidetails.loc[file, 'Site']):
        loca_in_wiki = accidetails.loc[file,'Site']
        split_to_pcs = str(loca_in_wiki).split('/')[0:9]
        if ';' in split_to_pcs[-1]:
            try:
                # Here we clean from un-wanted comments in the last part of Site:
                split_to_pcs[-1] = ''.join([chr for chr in split_to_pcs[-1] if chr in '0123456789.;'])
                latitude, longitude = map(float, split_to_pcs[-1].split(';'))
            except ValueError:
                pass
            else:
                accidetails.loc[file,'latitude'] = latitude
                accidetails.loc[file,'longitude'] = longitude
                loops_done[0] += 1


    # Here we try get-lat-long function with the first part of Site, to the second comma:
        if not pd.isna(accidetails.loc[file, 'Site']) and pd.isna(accidetails.loc[file, 'latitude']):          
            if __name__ == "__main__":
                if len(split_to_pcs) >= 2:
                    location_name = split_to_pcs[0]+','+ split_to_pcs[1]
                else:
                    location_name = split_to_pcs[0]
                for x in range(3):
                    for unwanted in eliminate:
                        location_name = location_name.replace(unwanted,'')
                if  get_lat_lon(location_name)[0]:
                    accidetails.loc[file,'latitude']  = get_lat_lon(location_name)[1]
                    accidetails.loc[file,'longitude'] = get_lat_lon(location_name)[2]
                    loops_done[1] +=1

    print('So now I just geo-optized',file)


# Below we clean the crucial columns and make sure they are numeric by duplicating them suffix _num:
    
new_columns = ['Passengers_num', 'Crew_num', 'Fatalities_num', 'Injuries_num', 'Survivors_num', 'Ground fatalities_num', 'Ground injuries_num']
accidetails[new_columns] = np.nan

col_to_clean = ['Passengers','Crew','Fatalities','Injuries','Survivors','Ground fatalities','Ground injuries']

split_and_drop = [' ',',', '(', '[', ';']

accidetails = accidetails.reset_index()

for i in range(len(accidetails)):
    for col in col_to_clean:
        if not pd.isna(accidetails.loc[i, col]):
            split_cell_data = str(accidetails.loc[i, col]).replace(' ','')
            for splitter in split_and_drop:
                if splitter in split_cell_data:
                    split_cell_data = split_cell_data.split(splitter)[0]
            try:
                accidetails.loc[i, col+'_num'] = int(split_cell_data)
            except:
                accidetails.loc[i, col+'_num'] = np.nan
            else:    
                accidetails.loc[i, col+'_num'] = int(split_cell_data)
        else:
            accidetails.loc[i, col+'_num'] = np.nan    
    
    # split_cell_data)
"""    
# Above we initially scrape all headings in infobox, the ones immediately
below are kept for possible later imrpovements, the ones to be dropped
are in the next following list
 11  Aircraft name          216 non-null    object 
 12  Occupants              767 non-null    object 
 15  Missing                26 non-null     object 
 16  Total fatalities       162 non-null    object 
 17  Total survivors        54 non-null     object 
 18  Type                   60 non-null     object 
 19  Total injuries  88 non-null     object 
""" 
cols_to_drop = ['Registration', 'Destination', 'Flight origin', 
'Name', '1st stopover', '2nd stopover', 'Stopover', 'Last stopover', '3rd stopover', 
'4th stopover', '5th stopover', '6th stopover', 'IATA flight No.', 'ICAO flight No.', 
'Call sign', 'Accused', 'Convicted', 'Charges', 'Verdict', 'Sentence', 'Passengers', 
'Crew', 'Fatalities', 'Survivors', 'Ground fatalities', 'Ground injuries', 'Injuries']    

for col in cols_to_drop:
    if col in accidetails.columns:
        accidetails.drop(columns=col, inplace=True)


accidetails['pax_onboard_num'] = (accidetails['Passengers_num'].fillna(0) + 
                               accidetails['Crew_num'].fillna(0))
                            # .astype(accidetails['Passengers'].dtype)

# Use np.NAN for missing values in death_rate and injury_rate


accidetails['death_rate'] = accidetails.apply(lambda row: 
                     row['Fatalities_num'] / row['pax_onboard_num'] if 
                     (row['pax_onboard_num'] != 0 and 
                      not pd.isnull(row['Fatalities_num'])) 
                     else np.NAN, 
                     axis=1)

accidetails['injury_rate'] = accidetails.apply(lambda row: 
                     row['Injuries_num'] / row['pax_onboard_num'] if 
                     (row['pax_onboard_num'] != 0 and 
                      not pd.isnull(row['Injuries_num']))  
                     else np.NAN, 
                     axis=1)


accidetails.to_csv('list_from_step045-var1.csv') 


