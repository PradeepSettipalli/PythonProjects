import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.offline import iplot
# Set notebook mode to work in offline
pyo.init_notebook_mode()

data = pd.read_csv("USA_suicide_rates-1.csv") #read csv for plot1

trace = go.Scatter( # initialize scatter object
  x = data['Year'], 
  y = data['Total deaths per 100,000'], 
  marker =  {'color': 'green', 
    'symbol': 0, 
    'size': 8},
  mode="markers+lines",
  text=['Year: ' + str(i) for i in list(range(2002,2018))], # hover text
  name='Total suicide rate') 

trace1 = go.Scatter( # initialize scatter object
  x = data['Year'], 
  y = data['Males deaths per 100,000'], 
  marker =  {'color': 'deepskyblue', 
    'symbol': 0, 
    'size': 8},
  mode="markers+lines",
  text=['Year: ' + str(i) for i in list(range(2002,2018))], # hover text
  name='Suicide rate in Males') 

trace2 = go.Scatter( # initialize scatter object
  x = data['Year'], 
  y = data['Females deaths per 100,000'], 
  marker =  {'color': 'hotpink', 
    'symbol': 0, 
    'size': 8},
  mode="markers+lines",
  text=['Year: ' + str(i) for i in list(range(2002,2018))], # hover text
  name='Suicide rate in Females') 



plotdata=go.Data([trace, trace1, trace2]) # Process the plots

layout=go.Layout(title="Age-adjusted Suicide Rates in United States",
  xaxis={'title':'Year'},  
  yaxis={'title':'Suicide rate'})  # design layout

figure=go.Figure(data=plotdata,layout=layout) # combine data and layout code
iplot(figure)

data1 = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv") #read csv for plot2

plotdata = go.Choropleth(
        locations = data1['CODE'],
        z = data1['GDP (BILLIONS)'], 
        text = data1['COUNTRY'],
        autocolorscale = False,
        colorscale = 'Picnic',
        showscale = True,
    ) # Process the plots
layout = go.Layout(
    title = "GDP of countries" # giving title to plot layout
    )

figure = go.Figure(data=[plotdata], layout=layout) # combine data and layout code
iplot(figure)


data2 = pd.read_csv("Estee_Lauder-1.csv") #read csv for plot3

trace = go.Bar( # initialize scatter object
  x = data2['Year'], # pass x, y values
  y = data2['Estee Lauder net income'],
  marker =  {'color': 'hotpink'}, # choose colour
    name='ESL') # name for legends

plotdata=go.Data([trace]) # Process the plots

layout=go.Layout(title="Estee Lauder Net Income", 
                 # configure the plot
  xaxis={'title':'Year'},  # layout and name
  yaxis={'title':'Income (Millions USD)'})  # the axes.

figure=go.Figure(data=plotdata,layout=layout)
# combine data and layout code

iplot(figure) # Render the plots