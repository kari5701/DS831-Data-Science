import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

app = dash.Dash(__name__)

data = pd.read_csv('list_from_step045.csv', encoding='utf-8')

types = data['Summary'].unique()
type_options = [{'label': i, 'value': i} for i in types]
type_options.append({'label': 'All acci Types', 'value': 'all'})

mintime = 1800
maxtime = 2025

# Generate the initial word cloud
wc_data = data['Summary'].dropna().tolist()
wc_text = ' '.join(wc_data)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wc_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('initial_wordcloud.png')  # Save the initial word cloud image


app.layout = html.Div([
    html.H1(children="Civil aviation accidents",
            style={'textAlign': 'center', 'font-family': 'Roboto'}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='summary1',
            options=type_options,
            value='all'),
            style={'width': '30%', 'display': 'inline-block', 'margin': '1%'}),
        # html.Div(dcc.Dropdown(
        #     id='summary2',
        #     options=type_options,
        #     value='all'),
        #     style={'width': '30%', 'display': 'inline-block', 'margin': '1%'}),
        html.Div(dcc.Dropdown(
            id='summary3',
            options=[True, False],
            value=True),
            style={'width': '30%', 'display': 'inline-block', 'margin': '1%'}),         
    ]),
    
    
    html.Div([
        html.H3(children="20231203-2112 GR13 working-well unfinished acci-dash",
                style={'textAlign': 'center', 'font-family': 'Roboto', 'color': 'red'}),
        html.Div([
            html.Div([
                dcc.Graph(id='acci-map')
            ], style={'width': '46%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '2%'}),
            html.Div([
                html.Div(id='wiki-info')
            ], style={'width': '46%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '2%'})
        ]),
        html.Div([
            dcc.RangeSlider(
                id='accident-dates',
                min=mintime,
                max=maxtime,
                step=25,
                value=[mintime, maxtime],
                marks={i: str(i) for i in range(mintime, maxtime, 25)})
        ]),
        html.Div([
            html.Div([dcc.Graph(id='word-cloud', figure={'data': [{'x': [], 'y': []}], 'layout': {'title': 'Initial Word Cloud'}})],
                     style={'width': '90%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '2%'}),
        ])
    ])
])

@app.callback(
    Output(component_id='acci-map', component_property='figure'),
    [
        Input(component_id='summary1', component_property='value'),
        Input(component_id='accident-dates', component_property='value')
    ]
)
def update_output(acci_type, acci_date):
    mydata = data
    if acci_type != 'all':
        mydata = data[data['Summary'] == acci_type]
    if acci_date != [mintime, maxtime]:
        mydata = mydata[(mydata['year'] >= acci_date[0]) & (mydata['year'] <= acci_date[1])]
    fig = px.scatter_mapbox(data_frame=mydata,
                            lat="latitude",
                            lon="longitude",
                            hover_name="acciname",
                            hover_data= ["Summary", "year", "Fatalities_num"],
                            size=[1 for i in mydata['Fatalities_num']],
                            size_max=10,
                            color="Fatalities_num",  # Specify the column for color,
                            # size=['Fatalities_num'],  could not make this work 20231125-2359, investigate!!!
                            zoom=0,
                            height=700,
                            mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 20, "b": 0}, coloraxis_showscale=False)
    return fig

@app.callback(Output('wiki-info', 'children'),
              [Input('acci-map', 'clickData')])
def update_wiki(click_data):
    url = "https://en.wikipedia.org/wiki/Aviation_accidents_and_incidents"
    if click_data != None:
        url = "https://en.wikipedia.org/wiki/" + click_data['points'][0]['hovertext'].replace(" ", "_")
    return [
        html.Iframe(src=url, style={'width': '100%', 'height': '700px', 'display': 'inline-block'})
    ]


# Callback for updating the word cloud
@app.callback(
    Output(component_id='word-cloud', component_property='figure'),
    [Input('summary3', 'clickData')]
)
def update_wordcloud(click_data):
    wc_data = data['Summary'].dropna().tolist()
    wc_text = ' '.join(wc_data)
    # testdata = data['Summary'].dropna()
    # text = " ".join(testdata)
    #  ************ hvor f..... tager denne update sine data fra? KAn ikke se wc_data som argument!
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('updated_wordcloud.png')  # Save the updated word cloud image
    return fig     # her må der manlge nogle parametre??????????????
    # Return a new figure with the updated word cloud
    # return {'data': [{'x': [], 'y': []}], 'layout': {'title': 'Updated Word Cloud', 'images': [{'source': 'updated_wordcloud.png',
    #                                                                                               'x': 0.5, 'y': 0.5,
    #                                                                                               'xanchor': 'center',
    #                                                                                               'yanchor': 'middle'}]}}


if __name__ == '__main__':
    app.run_server(debug=False, port=8080)

