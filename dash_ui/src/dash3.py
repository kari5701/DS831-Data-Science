from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Function to create a histogram layout
def create_histogram(data):
    # Create the histogram using Plotly Express
    fig = px.histogram(
        data,
        x="Length",
        nbins=30,  # Adjust the number of bins as needed
        labels={"Length": "Song Length (seconds)"},
        title="Distribution of Song Lengths"
    )
    fig.update_layout(
        xaxis_title="Length (seconds)",
        yaxis_title="Number of Songs",
        clickmode="event+select"  # Enable click events
    )
    # Return the layout for the histogram
    return dcc.Graph(
        id="length-histogram",
        figure=fig
    )
