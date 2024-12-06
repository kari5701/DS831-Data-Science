from dash1 import html, dcc
import pandas as pd
import pathlib
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

# Load the dataset
csv_path = pathlib.Path("/Users/karinachristensen/Documents/GitHub/DS831-Data-Science/data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)

# Generate wordcloud image
def generate_wordcloud(data):
    genres_text = ' '.join(data['Genres'].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(genres_text)

    # Save to a buffer
    buffer = io.BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    buffer.seek(0)

    # Encode image to base64 for display in Dash
    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_image}"

# Create the wordcloud layout
wordcloud_image = generate_wordcloud(cleaned_data)

layout = html.Div([
    html.H3("Genres Wordcloud"),
    html.Img(src=wordcloud_image, id='wordcloud-img', style={'width': '80%', 'height': 'auto'}),
    dcc.Store(id='selected-genre', data=None)  # Store for storing the selected genre from wordcloud
])

