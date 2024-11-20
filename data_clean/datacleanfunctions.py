#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:50:18 2024

@author: kevinpetersen
"""
import pandas as pd 
import re

# --- Clean the "Release Date" column ---

# Function to clean citation markers from text
def remove_citations(text):
    if pd.isna(text):  # Handle NaN values
        return text
    return re.sub(r'\[\d+\]', '', text).strip()  # Removes [1], [2], etc.


# Function to clean citation markers from text
def remove_citationswcommas(text):
    if pd.isna(text):  # Handle NaN values
        return text
    # Match patterns like [1], [, 1, ], etc.
    return re.sub(r"\[, \d+, ]","", text).strip()

# Function to clean extra commas
def remove_extra_commas(text):
    if pd.isna(text):  # Handle NaN values
        return text
    # Replace consecutive commas (with optional whitespace) with a single comma
    cleaned_text = re.sub(r' ,', '', text)
    # Remove leading/trailing commas or spaces
    return cleaned_text.strip(', ')



# import final scrape csv as dataframe
final_scrape =  pd.read_csv('final_scrape.csv', encoding='utf-8')


# Apply the function to clean the 'Release Date' column
final_scrape['Release Date'] = final_scrape['Release Date'].apply(remove_citations)

# apply the function to clean the "Genres" column
final_scrape['Genres'] = final_scrape['Genres'].apply(remove_citationswcommas) 

# Apply the function to clean the "Genres" column for extra commas
final_scrape['Genres'] = final_scrape['Genres'].apply(remove_extra_commas)


#Option to name output csv
csv_name = "final_scrape18"



# Save the cleaned data back to a CSV file
final_scrape.to_csv(f'{csv_name}.csv', index=False)
print(f"{len(final_scrape)} Datapoints has been saved to {csv_name}.csv")


