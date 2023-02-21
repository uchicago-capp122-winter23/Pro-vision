# These are the packages. You may need to pip install some of them.
# These should be included in the virtual environment
from dash import Dash, dcc, html
import urllib.request, json 
import dash_bootstrap_components as dbc
import plotly.express as px 
import pandas as pd
import numpy as np
import requests
import openpyxl

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY]) # dbc.themes.DARKLY is an imported theme for the Dash

# Importing excel
raw_data = requests.get("https://uchicago.box.com/shared/static/mxv5z4eommsiaydm9rru69gj5avygxto.xlsx").content
# Reading file to pandas
cleanedData = pd.read_excel(raw_data, sheet_name = "Community areas", dtype={'Layer': str, 'Name': str, 'GEOID': int, 
                                                                      'HCSNS_2016-2018': str})
cleanedData = cleanedData.rename(columns={'Name': 'Community Area'}) 
# Getting rid of commas in the variable HCSNS_2016-2018
cleanedData['HCSNS_2016-2018'] = cleanedData['HCSNS_2016-2018'].str.replace(',','')
# Parsing HCSNS_2016-2018 to numeric
cleanedData['HCSNS_2016-2018'] = pd.to_numeric(cleanedData['HCSNS_2016-2018'], downcast='float')

# Setting general colors
colors = { 
    'bg': 'rgba(0,0,0,0)',
    'font': '#FFFFFF'
}

# Importing the city of chicago geojson community level map
with urllib.request.urlopen("https://uchicago.box.com/shared/static/0hyrwzbja479o01f0ke99b418zvsudjr.geojson") as url:
        chicagoMap = json.load(url)

fig = px.choropleth(
        cleanedData, # Socioeconomic data
        geojson = chicagoMap, # Community Level Geojson
        color = 'HCSNS_2016-2018', # Setting color intensity by the values of HCSNS_2016-2018 (i.e., safety variable)
        color_continuous_scale = 'PuBu', # Choosing color
        locations = 'Community Area', # Identifies locations from geojson
        featureidkey = "properties.pri_neigh", # Consider pri_neigh as key from geojson dictionary
        labels={'HCSNS_2016-2018': 'Number of people whom reported to feel safe'} # Labelling socioeconomic variable
        )
fig.update_geos(fitbounds = "locations", visible = False) # Maps shapefile boundary locations from geojson
fig.update_layout(
    paper_bgcolor = colors['bg'], # Sets transparent background
    plot_bgcolor = colors['bg'], # Sets transparent background
    font_color = colors['font'], # Sets font color
    margin = {"r":20,"t":20,"l":20,"b":20} # Sets boundaries of map
    ) 

# Structure of Dashboard
app.layout = html.Div(children = [
    html.H1('Pro-Vision', style = {'textAlign': 'center'}), # Main header
    html.H4('''
        Visualize the travel time-distance of public facilities/services on 
        socioeconomic data to identify vulnerabilities in the City of Chicago.
        ''', style = {'textAlign': 'center'}), # Main description
    html.P("Select a socioeconomic indicator:"), # Paragraph
    dcc.Graph( 
        id = 'map',
        figure = fig
    ) # Displaying map
])

# Runs app from terminal with "python3 app.py". Once you run the map, you can exit with 'ctrl + c'
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port='8090', debug = False) # If there is a port error you can change it to '8080'