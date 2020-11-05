"""
@author: pradeepsettipalli
"""

import pandas as pd
data1 = pd.read_csv('skinresults.csv') #read csv file with results and import as dataframe

#change column names
data1.columns = ['productName', 'startPrice', 'rating', 'ratingCount',
       'numberofSales', 'seller']

#remove string named sale to easily convert this column to float
data1['numberofSales'].replace({"1 sale": "1"}, inplace=True)

#convert string to float data type
data1['numberofSales'] = pd.to_numeric(data1['numberofSales'], downcast="float")

#create seperate dataframe and csv file for organic skincare only
data2 = data1[data1['productName'].astype(str).str.contains("organic|ORGANIC|Organic")] #create dataframe data2 for organic skincare if data1 contains specified string names in productName
data2.to_csv('organicskincare.csv', index=False) #create csv file for organic skincare

#create seperate dataframe and csv file for regular skincare only
data3 = data1.merge(data2,how='left', indicator=True) # adds a new column '_merge'
data3 = data3[(data3['_merge']=='left_only')].copy() #rows only in data1 and not data2
data3.to_csv('regularskincare.csv', index=False) #create csv file for regular skincare

#create rating category in data2 and data3
import numpy as np
data2['rating_category'] = pd.cut(x=data2['rating'], bins=[0, 1, 2, 3, 4, 5], labels=['0-1', '1-2', '2-3', '3-4', '4-5'])
data3['rating_category'] = pd.cut(x=data3['rating'], bins=[0, 1, 2, 3, 4, 5], labels=['0-1', '1-2', '2-3', '3-4', '4-5'])
#create price category in data2 and data3
data2['price_category'] = pd.cut(x=data2['startPrice'], bins=[0, 25, 50, 100, 150, 200, 900], labels=['0-25', '25-50', '50-100', '100-150', '150-200', '>200'])
data3['price_category'] = pd.cut(x=data3['startPrice'], bins=[0, 25, 50, 100, 150, 200, 400], labels=['0-25', '25-50', '50-100', '100-150', '150-200', '>200'])

#create product category in data1 based on productName using lambda
list1 = ["organic", "Organic", "ORGANIC"] #search for these words in productName
def organic(a):
    for i in list1:
        if i in a:
            return "Organic" 
    return "Regular" 
data1["product_category"] = data1.productName.apply(lambda x: organic(x))

#create rating category in data1
data1['rating_category'] = pd.cut(x=data1['rating'], bins=[0, 1, 2, 3, 4, 5], labels=['0-1', '1-2', '2-3', '3-4', '4-5'])
#create price category in data1
data1['price_category'] = pd.cut(x=data1['startPrice'], bins=[0, 25, 50, 100, 150, 200, 900], labels=['0-25', '25-50', '50-100', '100-150', '150-200', '>200'])

import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.offline import iplot
# Set notebook mode to work in offline
pyo.init_notebook_mode()

#group data2 and data3 by rating category value to know number of products in each category
organicrating=data2.groupby('rating_category')
regularrating=data3.groupby('rating_category')

#group data2 and data3 by price category value to know number of products in each category
organicprice=data2.groupby('price_category')
regularprice=data3.groupby('price_category')

#group data1 by product category value to know number of products in each category
skincare = data1.groupby('product_category')

#counts number of products in each product category - organic and regular for plot1
temp0 = skincare['productName'].count().reset_index().sort_values(by='product_category', ascending=True)

#counts number of products in each price category
temp1 = organicprice['productName'].count().reset_index().sort_values(by='productName', ascending=False)
temp2 = regularprice['productName'].count().reset_index().sort_values(by='productName', ascending=False)

#counts number of products sold by sellers in each rating category
temp3 = organicrating['productName'].count().reset_index().sort_values(by='productName', ascending=True)
temp4 = regularrating['productName'].count().reset_index().sort_values(by='productName', ascending=True)





# plot 1 - pie chart
colors = ['darkorange', 'mediumturquoise'] #choose colours
labels = temp0.product_category #choose labels of pie chart
values = temp0.productName #choose values of pie chart
data=[go.Pie(labels=labels, values=values)]  # initialize pie chart

#configure the plot
layout = go.Layout(title='Number of skincare products in Etsy website')  #give a title

figure = go.Figure(data=data, layout=layout) #combine data and layout code

#update layout
figure.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
iplot(figure) #render the plots






# plot 2 - bar chart - shows number of organic and regular products in each price category

trace1 = go.Bar( #initialize bar chart
  x = temp1.price_category, #pass x, y values
  y = temp1.productName,
  marker =  {'color': 'darkorange'}, #choose colour
  name='Organic products') #name for legends

trace2 = go.Bar( #initialize bar chart
  x = temp2.price_category, #pass x, y values
  y = temp2.productName,
  marker =  {'color': 'mediumturquoise'}, #choose colour
  name='Regular products') #name for legends

data=[trace1, trace2]

#configure the plot
layout = go.Layout(
    title='Price of products in Etsy website',
    xaxis=dict(
        title='Price'
    ),
    yaxis=dict(
        title='Number of products'
    ),
)

figure = go.Figure(data=data, layout=layout) #combine data and layout code
iplot(figure) #render the plots





# plot 3 - bar chart - shows number of organic and regular products in each rating category

trace3 = go.Bar( #initialize bar chart
  x = temp3.rating_category, #pass x, y values
  y = temp3.productName,
  marker =  {'color': 'darkorange'}, #choose colour
  name='Organic products') #name for legends

trace4 = go.Bar( ##initialize bar chart
  x = temp4.rating_category, #pass x, y values
  y = temp4.productName,
  marker =  {'color': 'mediumturquoise'}, #choose colour
  name='Regular products') #name for legends

data=[trace3, trace4]

#configure the plot
layout = go.Layout(
    title='Rating of sellers in Etsy website',
    xaxis=dict(
        title='Rating'
    ),
    yaxis=dict(
        title='Number of products'
    ),
)

figure = go.Figure(data=data, layout=layout)  #combine data and layout code
iplot(figure) #render the plots






#remove duplicate values for sellers in data1 to avoid inaccurate results
data4 = data1.sort_values('product_category', ascending=True) #sort values in data1 by product category and save as data4
data4 = data4.drop_duplicates(subset='seller', keep='first') #drop duplicates and save as data4
sellerdata = data4.groupby('product_category') #group data4 by product category

#calculate 'total' number of ratings for organic and regular skincare sellers
temp5 = sellerdata['ratingCount'].sum().reset_index().sort_values(by='product_category', ascending=True)
#calculate 'mean' number of ratings for organic and regular skincare sellers
temp6 = sellerdata['ratingCount'].mean().reset_index().sort_values(by='product_category', ascending=True)
#calculate 'total' number of sales for organic and regular skincare sellers
temp7 = sellerdata['numberofSales'].sum().reset_index().sort_values(by='product_category', ascending=True)
#calculate 'mean' number of sales for organic and regular skincare sellers
temp8 = sellerdata['numberofSales'].mean().reset_index().sort_values(by='product_category', ascending=True)
#calculate 'total' number of ratings for organic and regular skincare sellers
temp9 = skincare['startPrice'].mean().reset_index().sort_values(by='product_category', ascending=True)





# plot 4 - bar chart - shows 'total' number of ratings of organic and regular skincare sellers

trace5 = go.Bar( #initialize bar chart
  x = temp5.product_category, #pass x,y values
  y = temp5.ratingCount,
  marker =  {'color': 'lightblue'}) #choose colour

data=[trace5]

#configure the plot
layout = go.Layout(
    title='Total number of ratings of sellers per skincare category', #name title and axes 
    xaxis=dict(
        title='Product category'
    ),
    yaxis=dict(
        title='Total number of ratings'
    ),
)

figure = go.Figure(data=data, layout=layout) #combine data and layout code
iplot(figure) #render the plots





# plot 5 - bar chart - shows 'mean' number of ratings of organic and regular skincare sellers

trace6 = go.Bar( #initialize bar chart
  x = temp6.product_category, #pass x,y values
  y = temp6.ratingCount,
  marker =  {'color': 'pink'}) #choose colour

data=[trace6]

#configure the plot
layout = go.Layout(
    title='Average number of ratings of sellers per skincare category', #name title and axes
    xaxis=dict(
        title='Product category'
    ),
    yaxis=dict(
        title='Average number of ratings'
    ),
)

figure = go.Figure(data=data, layout=layout) #combine data and layout code
iplot(figure) #render the plots






# plot 6 - bar chart - shows 'total' number of sales of organic and regular skincare sellers

trace7 = go.Bar( #initialize bar chart
  x = temp7.product_category, #pass x,y values
  y = temp7.numberofSales,
  marker =  {'color': 'lightblue'}) #choose colour

data=[trace7]

#configure the plot
layout = go.Layout(
    title='Total number of sales of sellers per skincare category', #name title and axes
    xaxis=dict(
        title='Product category'
    ),
    yaxis=dict(
        title='Total number of sales'
    ),
)

figure = go.Figure(data=data, layout=layout) #combine data and layout code
iplot(figure) #render the plots






# plot 7 - bar chart - shows 'mean' number of sales of organic and regular skincare sellers

trace8 = go.Bar( #initialize bar chart
  x = temp8.product_category, #pass x,y values
  y = temp8.numberofSales,
  marker =  {'color': 'pink'}) #choose colour

data=[trace8]

#configure the plot
layout = go.Layout(
    title='Average number of sales of sellers per skincare category', #name title and axes
    xaxis=dict(
        title='Product category'
    ),
    yaxis=dict(
        title='Average number of sales'
    ),
)

figure = go.Figure(data=data, layout=layout) #combine data and layout code
iplot(figure) #render the plots






# plot 8 - bar chart - shows average price of organic and regular products

trace9 = go.Bar( #initialize bar chart
  x = temp9.product_category, #pass x,y values
  y = temp9.startPrice,
  marker =  {'color': 'slategray'}) #choose colour

data=[trace9]

#configure the plot
layout = go.Layout(
    title='Average price of products per skincare category', #name title and axes
    xaxis=dict(
        title='Product category'
    ),
    yaxis=dict(
        title='Average Price'
    ),
)

figure = go.Figure(data=data, layout=layout) #combine data and layout code
iplot(figure) #render the plots






#select organic products in data4 based on product category and save as data5
data5 = data4[data4['product_category'].astype(str).str.contains("Organic")]
organicseller=data5.groupby('seller') #group data5 by seller

#calculate 'total' number of sales for organic skincare sellers
temp10 = organicseller['numberofSales'].sum().reset_index().sort_values(by='numberofSales', ascending=False)
temp10 = temp10.head(n=10) #select only top 10 sellers

listA = []
for i in temp10.seller:
    small_data = data5.loc[data5['seller']==i, :]
    listA.append(float(small_data.rating)) #get rating value of top 10 sellers

    
    
    
    
# plot 9 - bar chart with scatter plot - shows best organic skincare sellers

trace10a = go.Bar( #initialize bar chart
  x = temp10.seller, #pass x,y values
  y = temp10.numberofSales,
  marker =  {'color': 'darkorange'}, #choose colour
  name='Sales') #name for legend

trace10b = go.Scatter( #initialize scatter object
  x = temp10.seller, #pass x,y values
  y = listA,
  marker =  {'color': 'black'}, #choose colour
  name='Rating', #name for legend
  yaxis='y2') 

plotdata=go.Data([trace10a,trace10b]) #process the plots

#configure the plot
layout=go.Layout(title="<b>Best Organic skincare sellers in Etsy website", #name title and axes
                 titlefont = {
    "size": 20
  },
                 
  xaxis={'title':"<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br> <b>Sellers", #increase distace between title and axis
         'showgrid':False},
  yaxis={'title':'<b>Sales',
         'showgrid':False},
  yaxis2={'title':"<b>Rating",
          'overlaying': 'y',
          'side':'right',
          'showgrid':False})

figure=go.Figure(data=plotdata,layout=layout) #combine data and layout code

figure.layout.update(legend=dict(x=0, y=1.13)) #make legend readable by relocating

#update layout
figure.layout.update(
    yaxis2 = dict(
        range = [4, 5], #specify range for yaxis2
        autorange = False
    )
)

iplot(figure) #render the plots





#select regular products in data4 based on product category and save as data6
data6 = data4[data4['product_category'].astype(str).str.contains("Regular")]
regularseller=data6.groupby('seller') #group data6 by seller

#calculate 'total' number of sales for regular skincare sellers
temp11 = regularseller['numberofSales'].sum().reset_index().sort_values(by='numberofSales', ascending=False)
temp11 = temp11.head(n=10) #select only top 10 sellers

listB = []
for i in temp11.seller:
    small_data1 = data6.loc[data6['seller']==i, :]
    listB.append(float(small_data1.rating)) #get rating value of top 10 sellers

    

    
    
# plot 10 - bar chart with scatter plot - shows best regular skincare sellers

trace11a = go.Bar( #initialize bar chart
  x = temp11.seller, #pass x,y values
  y = temp11.numberofSales,
  marker =  {'color': 'mediumturquoise'}, #choose colour
  name='Sales') #name for legend

trace11b = go.Scatter( #initialize scatter object
  x = temp11.seller, #pass x,y values
  y = listB,
  marker =  {'color': 'black'}, #choose colour
  name='Rating', #name for legend
  yaxis='y2') 

plotdata=go.Data([trace11a, trace11b]) #process the plots

#configure the plot
layout=go.Layout(title="<b>Best Regular skincare sellers in Etsy website", #name title and axes
                 titlefont = {
    "size": 20
  },
                 
  xaxis={'title':"<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br> <b>Sellers", #increase distace between title and axis
         'showgrid':False},
  yaxis={'title':'<b>Sales',
         'showgrid':False},
  yaxis2={'title':"<b>Rating",
          'overlaying': 'y',
          'side':'right',
          'showgrid':False})

figure=go.Figure(data=plotdata,layout=layout) #combine data and layout code

figure.layout.update(legend=dict(x=0, y=1.13)) #make legend readable by relocating

#update layout
figure.layout.update(
    yaxis2 = dict(
        range = [4, 5], #specify range for yaxis2
        autorange = False
    )
)

iplot(figure) #render the plots


