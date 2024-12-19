from dash import dcc
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import random
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Preprocess the genres
def prepare_wordcloud_data(df, keywords):
    genres = []
    for cell in df['Genres'].dropna():
        for genre in cell.replace("-", " ").split(", "):
            for keyword in keywords:
                if keyword in genre.lower():
                    genres.append(keyword.capitalize())
    return pd.DataFrame({'Genre': genres}).value_counts().reset_index(name='Count')
    

# def create_wordcloud(data):
    
#     text = data.to_string()
        
#     # Generate a word cloud image
#     wordcloud = WordCloud().generate(text)

#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")

#     # lower max_font_size
#     wordcloud = WordCloud(max_font_size=40).generate(text)
#     plt.figure()
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     return plt.show()


# Wordcloud generation using Plotly

def create_wordcloud(data, keywords):
    wordcloud_data = prepare_wordcloud_data(data, keywords)

    positions = [(random.random(), random.random()) for _ in range(len(wordcloud_data))]
    words = wordcloud_data['Genre'].tolist()
    raw_sizes = wordcloud_data['Count'].tolist()

    # Normalize font sizes
    min_size = 10
    max_size = 50
    sizes = np.log1p(raw_sizes)
    sizes = min_size + (sizes - sizes.min()) / (sizes.max() - sizes.min()) * (max_size - min_size)

    wordcloud = go.Scatter(
        x=[pos[0] for pos in positions],
        y=[pos[1] for pos in positions],
        mode='text',
        text=words,
        textfont={'size': sizes, 'color': 'black'},
        hoverinfo='text',
        hovertext=[f'{word}: {count}' for word, count in zip(words, raw_sizes)],
        marker={'opacity': 0},
        name="WordCloud"
    )

    layout = go.Layout(
        xaxis_visible=False,
        yaxis_visible=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    return dcc.Graph(
        id="wordcloud-graph",
        figure=go.Figure(data=[wordcloud], layout=layout),
    )