from dash import dcc, html, Input, Output
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd


# Funktion til at generere WordCloud-billede
def generate_wordcloud(data):
    # Kombiner genrer til en lang tekststreng
    text = ' '.join(data['Genres'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Konverter WordCloud til et base64-billede
    image_stream = io.BytesIO()
    plt.figure(figsize=(8, 4), dpi=300)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(image_stream, format='png', bbox_inches='tight')
    plt.close()
    return f"data:image/png;base64,{base64.b64encode(image_stream.getvalue()).decode()}"


# Funktion til at oprette WordCloud-komponent
def create_wordcloud_component(data):
    image = generate_wordcloud(data)
    return html.Img(id="wordcloud-image", src=image, style={"width": "100%", "cursor": "pointer"})


# Callback til at filtrere tabel baseret på WordCloud-klik
def register_wordcloud_callbacks(app, data):
    @app.callback(
        Output("getting-started-sort", 'rowData'),
        Input("wordcloud-image", "n_clicks")
    )
    def update_table_from_wordcloud(n_clicks):
        if not n_clicks:
            return data.to_dict("records")
        # Eksempel: implementér yderligere kliklogik her
        return data.to_dict("records")
