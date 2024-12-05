import plotly.graph_objects as go
import pandas as pd

# Load the CSV file
df = pd.read_csv('html_scrape.csv') #indsæt den rigtige csv!!

# Verify the column names
print(df.columns)

# Create the table figure
fig = go.Figure(data=[go.Table(
    header=dict(
        values=list(df.columns),  # Use the column names as header
        fill_color='yellow',       # Correct key for color
        align='left'             # Align text to the left
    ),
    cells=dict(
        values=[df['Title'], df['Artist(s)'], df['Release Date'], df['Genres'], df['Length'], df['Label']],
        fill_color='lavender',   # Correct key for color
        align='left'             # Align text to the left
    )
)])

import plotly.io as pio
pio.renderers.default = 'browser'  # Set the renderer to open in your browser

fig.show()  # Now it should open the table in your default web browser

# Display the table
fig.show()
