# DS831 Programming in Data Science: Project 1

This repository contains the implementation for **Project 1** of the DS831 course, focused on working with data from Billboard Hot 100 number-one singles scraped from Wikipedia.

## Project Overview

The project consists of two main components:

1. **Data Gathering and Storage**:
   - Scrape data from [Wikipedia's Billboard Hot 100 number-one singles](https://en.wikipedia.org/w/index.php?title=Category:Billboard_Hot_100_number-one_singles).
   - Store the retrieved data in a CSV file with the following columns:
     - `name`: Song title (e.g., "Shallow")
     - `artist(s)`: List of artist(s) (e.g., Lady Gaga and Bradley Cooper)
     - `release date`: Song release date (e.g., September 27, 2018)
     - `genres`: List of genres (e.g., rock, folk-pop, country)
     - `length`: Song duration in minutes and seconds (e.g., 3:37)
     - `label`: Record label (e.g., Interscope)
     - `songwriters`: List of songwriters
     - `producers`: List of producers
    
2. **Data Analysis and Visualization**:
   - Develop a graphical user interface (GUI) using Dash/Plotly with the following features:
     - An interactive table with sortable columns to display:
       - Title, artist, release date, genres, label, and length of each song.
     - A **word cloud** summarizing genres:
       - Clicking on a genre applies a filter to the table.
     - A **histogram chart** showing song lengths in seconds:
       - Bars represent the frequency of songs with specific lengths.
       - Clicking on a bar applies a filter to the table.
     - Additional creative functionalities:
       - Allow browsing songs by artists, producers, and songwriters.

## Deliverables

- **Deliverable #1 (Data Gathering & Storage)**:
  - Deadline: 29 November 2024, 16:00
- **Deliverable #2 (User Interface)**:
  - Deadline: 20 December 2024, 16:00

## Prerequisites

To run the project, ensure the following tools are installed:

- Python 3.8+

## Setup and Usage

1. Clone this repository:
   ```bash
   git clone <https://github.com/kari5701/DS831-Data-Science>
   cd DS831-Data-Science

2. Instal the requirements:
   ```bash
   pip install -r requirements.txt

2. Scrape the Wikipedia articles:
   ```bash
   python html_wiki_scrape.py
  This will generate a directory called billboard_articles, containing the HTML for all the Billboard articles in separate files.

4. Scrape the HTML files:
   ```bash
   python scrape.py
  This script usees the Beautifull Soup function from `function_artist.py` to gather the following data: `name`, `artist(s)`, `relase date`, `genres`, `length`, `label`, `songwriters`, `producers', 'composers' and 'lyricists'. The data is saved into a `.csv` file.

  For data cleaning, `scrape.py` imports functionality from `function_dataclean.py` at the bottom of the code.

The UI Dashboard is set up to Tailwind CSS, if Node.JS is already installed on your computer enter:

```bash
pip i
```

If you don't have Node.JS on your computer, go follow the Tailwind CSS documentation to get started with Tailwind CSS: https://tailwindcss.com/docs/installation
