import dash
from dash import dcc, html, Input, Output
import pandas as pd
from wordcloud import WordCloud
import plotly.express as px
import io
import base64

# Load the dataset
# Replace 'your_file.csv' with the actual filename
df = pd.read_csv('html_scrape.csv')

# Preprocess the genres
df['Genres'] = df['Genres'].fillna('Unknown')  # Handle missing genres
all_genres = df['Genres'].str.split(',').explode()  # Split and expand genres into individual rows
genre_counts = all_genres.value_counts()  # Count occurrences of each genre

# Generate the Word Cloud
def generate_wordcloud():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(genre_counts)
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    return base64.b64encode(img.getvalue()).decode()

wordcloud_image = generate_wordcloud()

# Create the Dash app --> (her skal den forbindes til tabellen og resten?) 
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Billboard Hot 100 number-one singles"),
    
    # Word cloud as an interactive image
    html.Div([
        html.Img(
            id="wordcloud", 
            src=f"data:image/png;base64,{wordcloud_image}",
            style={"width": "100%", "cursor": "pointer"}
        )
    ]),
    
    html.H2("Filtered Table"),
    
    # Data table to display results
    dcc.Graph(id="genre_table")
])

# Callback to filter the table when a genre is clicked
@app.callback(
    Output("genre_table", "figure"),
    Input("wordcloud", "n_clicks")
)
def update_table(n_clicks):
    # This is a placeholder; you need to integrate a genre selection mechanism here
    filtered_df = df  # Update to filter based on clicked genre
    fig = px.table(filtered_df)
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8053)
