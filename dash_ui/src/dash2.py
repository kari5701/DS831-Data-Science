from dash import dcc, html
import pandas as pd
import plotly.express as px

# Funktion til at forberede data til WordCloud
def prepare_wordcloud_data(df, keywords):
    genres = []
    for cell in df['Genres'].dropna():
        for genre in cell.replace("-", " ").split(", "):
            for keyword in keywords:
                if keyword in genre.lower():
                    genres.append(keyword.capitalize())
    return pd.DataFrame({'Genre': genres}).value_counts().reset_index(name='Count')

# Funktion til at lave WordCloud
def create_wordcloud(data, keywords):
    wordcloud_data = prepare_wordcloud_data(data, keywords)

    fig = px.scatter(
        wordcloud_data,
        x='Genre',  # Navngiv tydeligt kolonnen
        y='Count',
        size='Count',
        text='Genre',
        size_max=100,
        hover_data={'Genre': True, 'Count': True}
    )

    fig.update_traces(
        textposition='middle center',
        hovertemplate='<b>%{text}</b><br>Count: %{customdata[1]}<extra></extra>'
    )

    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=10, b=10)
    )

    return dcc.Graph(id="wordcloud-graph", figure=fig)
