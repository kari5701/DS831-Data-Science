import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import random

# Load the dataset
df = pd.read_csv('html_scrape.csv')

# Preprocess the genres
df['Genres'] = df['Genres'].fillna('Unknown')  # Handle missing genres
all_genres = df['Genres'].str.split(',').explode()  # Split and expand genres into individual rows
genre_counts = all_genres.value_counts()  # Count occurrences of each genre

# Word cloud generation using Plotly
def generate_wordcloud_scatter(genre_counts, max_words=50):
    # Limit the number of words to display (top N frequent genres)
    genre_counts = genre_counts.head(max_words)
    
    # Generate random positions for the words
    positions = []
    for _ in range(len(genre_counts)):
        x = random.random()
        y = random.random()
        positions.append((x, y))
    
    # Create a dictionary for the words and their frequencies
    words = genre_counts.index.tolist()
    raw_sizes = genre_counts.values

    # Logarithmic scaling to prevent too large or too small word sizes
    min_size = 10  # Minimum size for words
    max_size = 50  # Maximum size for words
    sizes = np.log1p(raw_sizes)  # Apply logarithmic transformation
    sizes = min_size + (sizes - sizes.min()) / (sizes.max() - sizes.min()) * (max_size - min_size)  # Normalize the sizes

    # Scatter plot to represent words
    wordcloud = go.Scatter(
        x=[pos[0] for pos in positions],
        y=[pos[1] for pos in positions],
        mode='text',
        text=words,
        textfont={'size': sizes, 'color': 'black'},  # Adjusted text color and scaled size
        hoverinfo='text'
   )

    layout = go.Layout(
        xaxis_visible=False,  # Hides grid, ticks, and zero lines for X-axis
    yaxis_visible=False,  # Hides grid, ticks, and zero lines for Y-axis
    margin=dict(l=0, r=0, t=0, b=0),  # Removes plot margins
    height=600,  # Set figure height
    paper_bgcolor='white',  # Background color (can be changed as needed)
    plot_bgcolor='white'    # Plot area background color
    )

    return go.Figure(data=[wordcloud], layout=layout)

# Generate word cloud data
fig_wordcloud = generate_wordcloud_scatter(genre_counts)

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Billboard Hot 100 number-one singles", style={"textAlign": "center", "marginBottom": "20px"}),

    # Word cloud scatter plot
    dcc.Graph(
        id="wordcloud-graph",
        figure=fig_wordcloud
    ),

    html.H2("Filtered Table", style={"textAlign": "center", "marginTop": "20px"}),

    # Table to show filtered results
    dcc.Graph(id="filtered-table")
])

# Callback to filter the table when a genre word is clicked
@app.callback(
    Output("filtered-table", "figure"),
    Input("wordcloud-graph", "clickData")  # Listen for click events on the graph
)
def update_table(click_data):
    if click_data is None:
        # Show all data if nothing is clicked
        filtered_df = df
    else:
        # Get the word (genre) that was clicked
        clicked_word = click_data['points'][0]['text']
        # Filter the DataFrame for rows containing the selected genre
        filtered_df = df[df['Genres'].str.contains(clicked_word, case=False, na=False)]

    # Create and return a table figure
    return go.Figure(data=[go.Table(
        header=dict(values=list(filtered_df.columns)),
        cells=dict(values=[filtered_df[col] for col in filtered_df.columns])
    )])


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8061)
