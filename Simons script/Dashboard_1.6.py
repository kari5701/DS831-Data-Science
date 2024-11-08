#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 09:43:05 2023

@author: simonnordby
"""

import pandas as pd
from dash import dash, dash_table
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import dash_bootstrap_components as dbc

# Dash app
app = dash.Dash(__name__)

# Setup the data and dataframe
data = pd.read_csv('aviation_accidents.csv', encoding='utf-8')
df = pd.DataFrame(data)

### For the word cloud ###

# Convert 'Summary' column to strings
df['Summary'] = df['Summary'].astype(str)
wc_text = ' '.join(df['Summary'])

# Create a word cloud
wc = WordCloud(width=800, height=400, background_color='white').generate(wc_text)

# Convert word cloud image to base64 - chatGPT 
wordcloud_image = BytesIO()
wc.to_image().save(wordcloud_image, format='PNG')
wordcloud_image_base64 = base64.b64encode(wordcloud_image.getvalue()).decode()

### For the tabel ###

# Subsetting dataframe for the table 
selected_columns = ['Year', 'Name', 'Operator', 'Death Rate']
subset_df = df[selected_columns]


mintime = 1800
maxtime = 2025

########### Layout ############

app.layout = html.Div([
    # Header 1
    html.H1(children="Civil Aviation Accidents", style={'textAlign': 'center', 'font-family': 'Roboto'}),    
    
    html.Div([
        # Header 2
        html.H2(children="Accident Causes", style={'textAlign': 'center', 'font-family': 'Roboto'}),
        # Word Cloud
        html.Img(src='data:image/png;base64,{}'.format(wordcloud_image_base64),
                 style={'width': '70%', 'height': 'auto', 'margin': 'auto', 'display': 'block'}),
        # Accident Map
        html.Div([        
            dcc.Graph(id='accident_map')
            ], style={'width': '46%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '2%'}),
        # Wikipedia-html
        html.Div([
            html.Div(id='wiki_html')
            ], style={'width': '46%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '2%'})
        ]),
    # RangeSlider    
    html.Div([
            dcc.RangeSlider(
                id='accident_dates',
                min=mintime,
                max=maxtime,
                step=25,
                value=[mintime, maxtime],
                marks={i: str(i) for i in range(mintime, maxtime, 25)})
        ]),
        # Table
        html.Div([
        dbc.Container([
            dbc.Label('Click a cell in the table:'),
            dash_table.DataTable(
                subset_df.to_dict('records'),
                columns=[{"name": col, "id": col} for col in selected_columns],
                id='table',
                style_table={'overflowY': 'auto', 'maxWidth': '75%'},
                style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': 'lightblue'},
                page_size=10000,
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                selected_rows=[],
            ),
            dbc.Alert(id='tbl_out'),
        ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '2%'}),
        
        # Pie-chart
        dcc.Graph(id='pie_chart', style={'width': '35%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '0%'}),
    ])
])

########### Callbacks ############

# Accident Map
@app.callback(
    Output(component_id='accident_map', component_property='figure'),
    [Input(component_id='accident_dates', component_property='value')
     ])

# Function for Accident map
def update_output(accident_date):
    mydata = data
    if accident_date != [mintime, maxtime]:
        mydata = mydata[(mydata['Year'] >= accident_date[0]) & (mydata['Year'] <= accident_date[1])]
    fig = px.scatter_mapbox(data_frame=mydata,
                            lat="Latitude",
                            lon="Longitude",
                            hover_name="Name",
                            hover_data=["Year","Summary", "Fatalities"],
                            size=[1 for i in mydata['Fatalities']],
                            size_max=10,
                            color="Fatalities",
                            zoom=0,
                            height=700,
                            mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 20, "b": 0}, coloraxis_showscale=False)
    return fig

# Wikipedia html
@app.callback(Output(component_id = 'wiki_html', component_property = 'children'),
             [Input(component_id = 'accident_map', component_property = 'clickData')]
              )

# Function for the wikipedia htmls
def update_wiki(click_data):
    url = "https://en.wikipedia.org/wiki/Aviation_accidents_and_incidents"
    if click_data:
        url = "https://en.wikipedia.org/wiki/" + click_data['points'][0]['hovertext'].replace(" ", "_")
    return [html.Iframe(src=url, style={'width': '100%', 'height': '700px', 'display': 'inline-block'})]


# Callback for table-data 
@app.callback (Output('tbl_out', 'children'), 
               Input('table', 'active_cell'))

# Function for table-data
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"


# Callback for pie Chart
@app.callback(
    Output("pie_chart", "figure"),  
    Input("table", "active_cell"))

# Function for pie chart
def generate_chart(active_cell): 
    # When clicking on a row, show the death rate of the corresponding row
    if active_cell:
        row = active_cell['row']
        selected_row = df.iloc[row]
        death_rate = selected_row['Death Rate']
        
        # Create the pie chart based on the death rate of the selected row
        fig = px.pie(values=[death_rate, 1 - death_rate], 
                     names=['Death Rate', 'Survival Rate'],
                     color_discrete_sequence=['red', 'blue']  # Assigning red color to 'Death Rate'
                     )
        return fig
    
    # If no cell is selected, show an empty pie-chart
    return px.pie(values=[0, 100], names=['Death Rate', 'Survival Rate'])


# Run app
if __name__ == '__main__':
    app.run_server(debug=False, port=8080)
