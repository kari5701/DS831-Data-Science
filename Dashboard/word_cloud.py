#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 18:44:51 2023

@author: simonnordby
"""
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import dash
from dash import dcc, html

# Setup the data and dataframe
data = pd.read_csv('volcanos.csv', encoding='utf-8')
df = pd.DataFrame(data)

# Inside the wordcloud -> the 'country' text column
text = ' '.join(df['country'])

# Create a word cloud
wc = WordCloud(width=800, height=400, background_color='white').generate(text)

# Convert word cloud image to base64 - chatGPT 
wordcloud_image = BytesIO()
wc.to_image().save(wordcloud_image, format='PNG')
wordcloud_image_base64 = base64.b64encode(wordcloud_image.getvalue()).decode()

# Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Volcano Word Cloud"),
    html.Img(src='data:image/png;base64,{}'.format(wordcloud_image_base64),
             style={'width': '80%', 'height': 'auto', 'margin': 'auto', 'display': 'block'})
])

if __name__ == '__main__':
    app.run_server(debug=False, port=8080)
