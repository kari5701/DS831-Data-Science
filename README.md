# DS831 Programming in Data Science: Project 1

This repository contains the implementation for **Project 1** of the DS831 course, focused on working with data from Billboard Hot 100 number-one singles scraped from Wikipedia.

## Prerequisites

To run the project, ensure the following tools are installed:

- Python 3.8+

## Setup and Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/kari5701/DS831-Data-Science

2. Instal the requirements:
   ```bash
   pip install -r requirements.txt

3. Scrape the Wikipedia articles (it's possible to skip this part, as the project already contains these files):
   ```bash
   python multipage_scraper.py
  This will generate a directory called `billboard_articles`, containing the HTML for all the Billboard articles in separate files.

4. Parsing the HTML files and cleaning the data:
   ```bash
   python parse_and_clean.py
  This script usees the Beautifull Soup function from `artist_parse_func.py` to gather the following data: `name`, `artist(s)`, `relase date`, `genres`, `length`, `label`, `songwriters`, `producers`, `composers` and `lyricists`. Columns are then cleaned using extract and replace.str. DataTypes are convertet The data is saved into a `.csv` file.

5. Dashboard UI 
    ```bash
   python app.py
  The dashboard uses constants from src/`const.py` containing the `html_cleaned.csv`and importing modules from the `viz_functions` as functions to display the cleaned data.
