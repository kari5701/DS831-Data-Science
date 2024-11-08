#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignment 3
@author: Group 13: Simon Nordby, Melek Unlu, Flemming Boye
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
# from dash_table.Format import Format, Scheme FBOY: Remove again, 
# tried to make some data display as % in table

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

# Convert word cloud image to base64 - chatGPT  ***************** FBOY remove
wordcloud_image = BytesIO()
wc.to_image().save(wordcloud_image, format='PNG')
wordcloud_image_base64 = base64.b64encode(wordcloud_image.getvalue()).decode()

### For the tabel ###

# Subsetting dataframe for the table 
selected_columns = ['Year', 'Name', 'Operator', 'Fatalities', 'Death Rate', 'Injury Rate']
subset_df = df[selected_columns]
subset_df['Death Rate']  = subset_df['Death Rate'].round(decimals = 3)
subset_df['Injury Rate'] = subset_df['Injury Rate'].round(decimals = 3)
# subset_df['Year'].astype(str)  # FBOY tried to see if this solves filtering by yeara problem

#  FBOY-ChatGPT 20231213-1130: Calculate column widths based on content length
column_widths = {col: max(subset_df[col].astype(str).apply(lambda x: len(x)).max(), len(col)) 
                 for col in selected_columns}

mintime = 1900
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
                step=5,
                value=[mintime, maxtime],
                marks={i: str(i) for i in range(mintime, maxtime, 5)})
        ]),
        # Table
        # FBOY I think it would be nice to include also 'Injured Rate' and maybe format
        # FBOY these last columns as pct (or if not then 0.+2 or 3 decimals)
        # FBOY maybe make narrow 'year' column to make room for above-mentioned, also 'Fatalities'
        html.Div([
        dbc.Container([
            dbc.Label('Click a cell in the table or apply filter by using the top, empty row:'),
            dash_table.DataTable(
                subset_df.to_dict('records'),
                columns=[{"name": col, "id": col} for col in selected_columns],
                id='table',
                style_table={'overflowY': 'auto', 'maxWidth': '75%'},
                style_cell={'textAlign': 'left', 'minWidth': '40px', 'width': '100px', 'maxWidth': '100px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': 'lightblue'},
                page_size=10000,  # FBOY tried with 50 but as Simon know it does not work
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                selected_rows=[],
                #   FBOY-ChatGPT 20231213-1130: Set individual column widths, works nicely :-)
                style_cell_conditional=[
                    {'if': {'column_id': col}, 'width': f'{column_widths[col]}px'} 
                    for col in selected_columns
                ],
                # FBOY this never worked for me, so this and following rows should be deleted....
                # # Format 'Death Rate' and 'Injury Rate' columns as percentages
                # style_data_conditional=[
                #     {'if': {'column_id': col}, 'type': 'numeric',
                #     'format': Format(precision=2, scheme=Scheme.fixed),
                # } for col in ['Death Rate', 'Injury Rate']
            # ],
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
        # FBOY this row and following 8-10 rows should be removed again !       
        # Filter the data based on the selected row's information
   
        selected_row = df.iloc[row]
        # FBOY inital row, rest to:        selected_row = df.iloc[row]
        death_rate  = selected_row['Death Rate']
        injury_rate = selected_row['Injury Rate']

        # FBOY this row and following 8-10 rows should be removed again !       
        # Filter the data based on the selected row's information
        # filtered_data = df[
        # (df['Year'] == selected_row['Year']) &
        # (df['Name'] == selected_row['Name']) &
        # (df['Operator'] == selected_row['Operator']) &
        # (df['Fatalities'] == selected_row['Fatalities']) &
        # (df['Death Rate'] == selected_row['Death Rate']) &
        # (df['Injury Rate'] == selected_row['Injury Rate'])
        # ]
        
        # Create the pie chart based on the death rate of the selected row
        # FBOY we shall have the 'Injury Rate' and 'Unhurt' incorporated into the folling rows
        fig = px.pie(values=[death_rate, injury_rate, 1 - death_rate - injury_rate], 
                     names=['Death Rate', 'Injury Rate', 'Unhurt Rate'],
                     color_discrete_sequence=['red', 'yellow', 'green'],  
                     # Assigning red color to 'Death Rate' etc.:
                     category_orders={'names': ['Death Rate', 'Injury Rate', 'Unhurt Rate']}
                     )
        # Add a title to the pie chart
        fig.update_layout(title=f"{selected_row['Name']}")
        return fig
    
    # If no cell is selected, show an empty pie-chart
    return px.pie(values=[33, 33, 33], names=['Death Rate', 'Injury Rate', 'Unhurt Rate'],
                  color_discrete_sequence=['red', 'yellow', 'green'])


# Run app
if __name__ == '__main__':
    app.run_server(debug=False, port=8080)
