import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from plotly.offline import plot

app = dash.Dash(__name__)

data = pd.read_csv('list_from_step045.csv', encoding='utf-8')
data['Fatalities_num'] = data['Fatalities_num'].dropna()

selected_columns = ['local_file', 'year', 'link-in-year', 'acciname', 'accihref',
       'has_infobox', 'Date', 'Summary', 'Site', 
       'Aircraft type', 'Passengers_num', 'Crew_num', 'Fatalities_num',
       'Survivors_num', 'Ground fatalities_num', 'Ground injuries_num']

testdata = data[selected_columns]

testdata = testdata.query('Fatalities_num >= 200').sort_values('Fatalities_num', 
                                                              ascending = False)
fig1 = px.pie(testdata, values='Fatalities_num', names='acciname', title='Larger accidents #fatalities')

plot(fig1)






# fig1.show()
    

# testdata2 = testdata.groupby('year').sum()


# statistik = testdata.describe(include='all')

# testdata.to_excel('testdata.xlsx')
# testdata2.to_excel('testdata2.xlsx')
# # statistik.to_excel('stat paa testdata.xlsx')      

# df = px.testdata # .gapminder().query("year == 2007")  
# .query("continent == 'Europe'")
# df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
      