from dash import dcc
import pandas as pd
import plotly.express as px

# Funktion til at forberede data til histogram
def prepare_histogram_data(df, keywords):
    genres = []
    for cell in df['Genres'].dropna():
        for genre in cell.replace("-", " ").split(", "):
            for keyword in keywords:
                if keyword in genre.lower():
                    genres.append(keyword.capitalize())
    return pd.DataFrame({'Genre': genres}).value_counts().reset_index(name='Count')

# Funktion til at lave histogram
def create_histogram(data, keywords):
    histogram_data = prepare_histogram_data(data, keywords)

    fig = px.bar(
        histogram_data,
        x='Genre',
        y='Count',
        text='Count',
        hover_data={'Genre': True, 'Count': True}
    )

    fig.update_traces(
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Genre",
        yaxis_title="Count",
        margin=dict(l=10, r=10, t=10, b=10)
    )

    return dcc.Graph(id="histogram-graph", figure=fig)
