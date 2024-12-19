import plotly.graph_objs as go
import plotly.express as px
import dash_ag_grid as dag
import pandas as pd
import numpy as np
import random

# Define column definitions based on your dataset
columnDefs = [
    {'field': 'Title', 'headerName': 'Song Title'},
    {'field': 'Artist(s)', 'headerName': 'Artists'},
    {'field': 'Release Date', 'headerName': 'Release Date'},
    {'field': 'Genres', 'headerName': 'Genres'},
    {'field': 'Length', 'headerName': 'Song Length'},
    {'field': 'Label', 'headerName': 'Label'},
    {'field': 'Songwriters', 'headerName': 'Songwriters'},
    {'field': 'Producers', 'headerName': 'Producers'},
]
# Function to create a grid layout
def create_grid(data):
    grid = dag.AgGrid(
        style={"height": 800},
        id="getting-started-sort",
        rowData=data.to_dict("records"),
        columnDefs=columnDefs,
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
        dashGridOptions={'animateRows': False,
                         'pagination': True,
                         'paginationPageSize': 18
        },
    )
    return grid

def prepare_genre_data(df, keywords):
    """Helper function to prepare genre data for histogram and wordcloud"""
    genres = []
    for cell in df['Genres'].dropna():
        for genre in cell.replace("-", " ").split(", "):
            for keyword in keywords:
                if keyword in genre.lower():
                    genres.append(keyword.capitalize())
    return pd.DataFrame({'Genre': genres}).value_counts().reset_index(name='Count')

# Creating a length histogram:
def create_length_histogram(data):
    fig = px.histogram(
        data,
        x="total_seconds",
        labels={"Length": "Song Length (seconds)"},
        title="Distribution of Song Lengths",
        marginal="rug",
    )
    
    fig.update_layout(
        xaxis_title="Length (seconds)",
        yaxis_title="Number of Songs"
    )
    
    return fig

# Creating a genre-histogram:
def create_genre_histogram(data, keywords):
    histogram_data = prepare_genre_data(data, keywords)
    fig = px.bar(
        histogram_data,
        x="Genre",
        y="Count",
        text="Count",
        hover_data={'Genre': True, 'Count': True},
        title="Genre Distribution",

    )
    fig.update_traces(
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title="Genre",
        yaxis_title="Count",
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

# Wordcloud generation using Plotly (NOT EXPRESS)
def create_wordcloud(data, keywords):
    """Creates the wordcloud figure"""
    wordcloud_data = prepare_genre_data(data, keywords)
    
    positions = [(random.random(), random.random()) for _ in range(len(wordcloud_data))]
    words = wordcloud_data['Genre'].tolist()
    raw_sizes = wordcloud_data['Count'].tolist()

    # Normalize font sizes
    min_size = 10
    max_size = 50
    sizes = np.log1p(raw_sizes)
    sizes = min_size + (sizes - sizes.min()) / (sizes.max() - sizes.min()) * (max_size - min_size)

    wordcloud = go.Figure()
    
    wordcloud.add_trace(go.Scatter(
        x=[pos[0] for pos in positions],
        y=[pos[1] for pos in positions],
        mode='text',
        text=words,
        textfont={'size': sizes, 'color': 'black'},
        hoverinfo='text',
        hovertext=[f'{word}: {count}' for word, count in zip(words, raw_sizes)],
        marker={'opacity': 0},
        name="WordCloud"
    ))

    wordcloud.update_layout(
        xaxis_visible=False,
        yaxis_visible=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    return wordcloud