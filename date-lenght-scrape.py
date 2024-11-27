#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 10:14:27 2024

@author: indira
"""

import pandas as pd
import re
import time
from datetime import datetime

# Cleaning the Release Date column
def clean_date(date):
    if pd.isna(date):
        return None

    date = re.sub(r'\(.*?\)', '', date).strip()

    try:
        parsed_date = pd.to_datetime(date, errors='coerce', dayfirst=False)
        if pd.notna(parsed_date):
            return parsed_date.strftime('%B %d, %Y')  # Format: Month Day, Year
    except Exception:
        pass

    return date

df['Release Date'] = df['Release Date'].apply(clean_date)

# Cleaning the Length column
def time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except Exception:
        return 0

def seconds_to_time(total_seconds):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"

#clean lenght function
def clean_length(length):
    if pd.isna(length):
        return None

    # Remove anything in parentheses to simplify
    length = re.sub(r'\(.*?\)', '', length).strip()

    # PRIORITY 1: Check for "single version"
    if "single version" in length.lower():
        print(f'single version in {length}')
        match = re.search(r'single version.*?(\d+:\d{2})', length, re.IGNORECASE)
        if match:
            return match.group(1)

    # PRIORITY 2: clean multiple parts (e.g: "Part 1, 2, 3")
    if 'part' in length.lower():
        print(f'part in {length}')
        parts = re.split(r'[;/and]', length)  # Split on delimiters like ";", "/", or "and"
        for part in parts:
            if "part 1" in part.lower():  # Look for Part 1 specifically
                match = re.search(r'(\d+:\d{2})', part)
                if match:
                    return match.group(1)

    # PRIORITY 3: if no "single version or part version" fall back to the first valid time
    match = re.search(r'(\d+:\d{2})', length)  # Grab the first valid time if no "single version" or "part 1" exists
    if match:
        return match.group(1)

    # If no valid time is found
    return None


df['Length'] = df['Length'].apply(clean_length)


df.to_csv('finalll_scrapee_cleaned.csv', index=False)
print("Data has been cleaned and saved to finalll_scrapee_cleaned.csv")
