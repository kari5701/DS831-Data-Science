from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import dash_ag_grid as dag
from src.Constants import csv_path, clean_genres, KEYWORDS, columnDefs
from src.Viz_functions import create_length_histogram, create_genre_histogram, create_wordcloud


# Load the CSV file into a DataFrame
cleaned_data = pd.read_csv(csv_path)
cleaned_data['Genres'] = cleaned_data['Genres'].fillna("")

# Genre List
GENRES = clean_genres(cleaned_data, KEYWORDS)

# Initialize the Dash app
app = Dash(__name__)


# Define app layout
app.layout = html.Div([ #main container
    html.Div( # header container
        [
        html.Div(html.Img(src="assets/Billboard_logo.png", width=300, style={ #Logo
            'padding': '10px'
            }
                          )
                 ),
        html.H1('Analysis', style={ #H1 text
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
            "sortable": True,
            "wrapHeaderText": True,
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
    html.Div([
        html.Div(id='output'),
        html.Button('Input',id='input_button',n_clicks=0),
        html.Button('Reset',id='reset_button', n_clicks=0),
        ], style={'marginTop':20, 'marginLeft':20}
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


# The one callback-funcion to update by genre:
@callback(
    [
        Output("song-grid", "rowData"),
        Output("length-histogram", "figure"),
        Output("genre-histogram", "figure"),
        Output("wordcloud-graph", "figure"),
        Output("genre-dropdown", "value"),
    ],
    [
        Input('genre-dropdown', 'value'),
        Input("wordcloud-graph", "clickData"),
    ]
)
def update_all(selected_genres, clickData):
    filtered_data = cleaned_data.copy()

    # Filter by selected genres from dropdown
    if selected_genres and len(selected_genres) > 0:
        regex_pattern = '|'.join(selected_genres)
        filtered_data = filtered_data[filtered_data['Genres'].str.contains(regex_pattern, case=False, na=False)]

    # filter by word clicked in the word cloud
    selected_word = ""
    if clickData and 'points' in clickData and len(clickData['points']) > 0:
        selected_word = clickData['points'][0].get('text', '')
        if selected_word:
            filtered_data = filtered_data[filtered_data['Genres'].str.contains(selected_word, case=False, na=False)]

    # Update dropdown value if a word is selected
    if selected_word and selected_word not in selected_genres:
        selected_genres = selected_genres + [selected_word] if selected_genres else [selected_word]

    row_data = filtered_data.to_dict("records")
    length_histogram = create_length_histogram(filtered_data)
    genre_histogram = create_genre_histogram(filtered_data, KEYWORDS)
    wordcloud = create_wordcloud(filtered_data, KEYWORDS)

    return row_data, length_histogram, genre_histogram, wordcloud, selected_genres

selected_word = ""

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)