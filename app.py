from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import pathlib
import dash_ag_grid as dag
from src.Constants import clean_genres, KEYWORDS, columnDefs
from src.Viz_functions import create_length_histogram, create_genre_histogram, create_wordcloud


# Load the CSV file into a DataFrame
csv_path = pathlib.Path("data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)
cleaned_data['Genres'] = cleaned_data['Genres'].fillna("")

# Genre List
GENRES = clean_genres(cleaned_data, KEYWORDS)

# Initialize the Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    # Header
    html.Div(
        [
        html.Div(html.Img(src="assets/Billboard_logo.png", width=300, style={
            'padding': '10px'
            }
                          )
                 ),
        html.H1('Analysis', style={
            'color': 'black', 
            'fontFamily': 'Arial, sans-serif',
            'backgroundColor': 'white',
            'padding': '10px'
            }
                )
        ]
             ),
    
    # Grid Component
    dag.AgGrid(
        id="song-grid",
        style={"height": 600},
        columnDefs=columnDefs,
        rowData=cleaned_data.to_dict("records"),
        columnSize="sizeToFit",
        defaultColDef={
            "filter": True,
            "floatingFilter": True,
            "sortable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
            "initialWidth": True,
            "resizable": True,
            },
        dashGridOptions={
            'animateRows': False,
            'pagination': True,
            'paginationPageSize': 18
            },
        ),
    
    # Dropdown for Genres
    dcc.Dropdown(
        id='genre-dropdown',
        style={'fontFamily': 'Arial, sans-serif'},
        options=[{'label': genre, 'value': genre} for genre in GENRES],
        placeholder='Select a genre',
        multi=True,
        value=[]
        ),
    
    # histogram container with better spacing and layout
    html.Div([
        # Row 1 - Histograms
        html.Div([
            # Column 1 - Length Histogram
            html.Div([
                dcc.Graph(
                    id='length-histogram',
                    figure=create_length_histogram(cleaned_data)
                )
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            # Column 2 - Genre Histogram
            html.Div([
                dcc.Graph(
                    id='genre-histogram',
                    figure=create_genre_histogram(cleaned_data, KEYWORDS)
                )
            ], style={'width': '50%', 'display': 'inline-block'})
        ]),
        
        # Row 2 - Wordcloud component
        html.Div([
            dcc.Graph(
                id='wordcloud-graph',
                figure=create_wordcloud(cleaned_data, KEYWORDS)
            )
        ])
    ], style={'padding': '20px'})
])

# define callback functions:

#  allback to update AgGrid based on dropdown or WordCloud click
@callback(
    Output("song-grid", "rowData"),
    [Input('genre-dropdown', 'value'),
     Input("wordcloud-graph", "clickData")]  # Updated to match new ID
)
def update_grid(selected_genres, clickData):
    filtered_data = cleaned_data.copy()
    
    if selected_genres and len(selected_genres) > 0:
        regex_pattern = '|'.join(selected_genres)
        filtered_data = filtered_data[filtered_data['Genres'].str.contains(regex_pattern, case=False, na=False)]
    
    if clickData and 'points' in clickData and len(clickData['points']) > 0:
        selected_word = clickData['points'][0].get('text', '')
        if selected_word:
            filtered_data = filtered_data[filtered_data['Genres'].str.contains(selected_word, case=False, na=False)]
    
    return filtered_data.to_dict('records')

@callback(
    Output("length-histogram", "figure"),
    Input('genre-dropdown', 'value')
)
def update_length_histogram(selected_genres):
    filtered_data = cleaned_data.copy()
    
    if selected_genres and len(selected_genres) > 0:
        regex_pattern = '|'.join(selected_genres)
        filtered_data = filtered_data[filtered_data['Genres'].str.contains(regex_pattern, case=False, na=False)]
    
    return create_length_histogram(filtered_data)

@callback(
    Output("genre-histogram", "figure"),
    Input('genre-dropdown', 'value')
)
def update_genre_histogram(selected_genres):
    filtered_data = cleaned_data.copy()
    
    if selected_genres and len(selected_genres) > 0:
        regex_pattern = '|'.join(selected_genres)
        filtered_data = filtered_data[filtered_data['Genres'].str.contains(regex_pattern, case=False, na=False)]
    
    return create_genre_histogram(filtered_data, KEYWORDS)

@callback(
    Output("wordcloud-graph", "figure"),
    Input('genre-dropdown', 'value')
)
def update_wordcloud(selected_genres):
    filtered_data = cleaned_data.copy()
    
    if selected_genres and len(selected_genres) > 0:
        regex_pattern = '|'.join(selected_genres)
        filtered_data = filtered_data[filtered_data['Genres'].str.contains(regex_pattern, case=False, na=False)]
    
    return create_wordcloud(filtered_data, KEYWORDS)

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)