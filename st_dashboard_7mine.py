#################################### NewYork CitiBikes Strategy Dashboard ############################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################################### Initial settings for the dashboard ######################################

st.set_page_config(page_title = 'NewYork CitiBikes Strategy Dashboard', layout='wide')
st.title("NewYork CitiBikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ##############################################################################

df = pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)


######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems NewYork CitiBikes currently faces.")
    st.markdown("Right now, NewYork CitiBikes has run into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("New York Bikes.jpg") 
    st.image(myImage)

########################################## DEFINE THE CHARTS ###############################################################


### Create the dual axis line chart page ###

elif page == 'Weather component and bike usage':

fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

fig_2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['bike_rides_daily'],
        name='Daily bike rides',
        line=dict(color='blue')  
    ),
    secondary_y=False
)

fig_2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['AVGTemperature (°C)'],
        name='Daily temperature',
        line=dict(color='red')  
    ),
    secondary_y=True
)

fig_2.update_layout(
    title='Daily Bike rides and temperatures in 2022',
    height=600
)

st.plotly_chart(fig_2, use_container_width=True)
st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

## Bar chart

df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station'], y = top20['value']))

fig = go.Figure(go.Bar(x = top20['start_station'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in NewYork',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see Grove St. PATH, South Waterfront  Walkway - Sinatra as well as Hoboken Terminal - River St & Hudson Pl. There is a big jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "New York CitiBikes Bikes Trips Aggregated.html" 

    # Read the file and store in variable
with open(path_to_html, 'r', encoding='utf-8') as f:
    html_data = f.read()
        
## Show in webpage
    st.header("Aggregated Bike Trips in NewYork")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("Grove St. PATH, South Waterfront  Walkway - Sinatra and Hoboken Terminal - River St & Hudson Pl. These stations show the highest number of bike trips, likely due to their proximity to one of New York’s busiest transportation hubs, with many commuters using bikes as part of their journey to and from work.")
    st.markdown("The top 3 stations are well-situated for both commuting (especially for those traveling from New Jersey to Manhattan) and recreational biking along the Hudson River. They provide essential links for getting around these areas, whether you’re heading toward transit, exploring parks, or simply enjoying a bike ride along the river.")

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("Citi.jpg")  
    st.image(bikes)
    st.markdown("### Our analysis has shown that CitiBikes should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the water line so as to have optimal distribution of bikes since these areas are hot spot start stations for riders.")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs")