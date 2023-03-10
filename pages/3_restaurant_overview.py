# Libraries

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static

st.set_page_config(page_title= "Restaurant View", page_icon = "🍽️", layout='wide')

# ==========================
# Functions
# ==========================

def distance(df1):
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']

    df1['distance'] = (df1.loc[:, cols].apply(lambda x:                                       haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1))
    avg_distance = np.round(df1['distance'].mean(),2)
    
    return avg_distance

def avg_std_time_delivery(df1, festival, op):
    """
        This function returns the delivery average time and standard deviation.
         Input:
         - df: Dataframe with required data to calculate
         - op: Type of operation: avg_time and std_time
         Output:
         - df: Dataframe with 2 columns and 1 row
    """    
    aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
              .groupby('Festival')
              .agg({'Time_taken(min)':['mean','std']}))

    aux.columns = ['avg_time', 'std_time']
    aux = aux.reset_index() 
    aux = np.round(aux.loc[aux['Festival'] == festival, op], 2)
            
    return aux

def avg_std_time_graph(df1):
    aux = df1.loc[:, ['City','Time_taken(min)']].groupby('City').agg({'Time_taken(min)':['mean','std']})
    aux.columns = ['avg_time', 'std_time']
    aux = aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                           x = aux['City'],
                           y = aux['avg_time'],
                     error_y = dict(type='data', array=aux['std_time'])))
    fig.update_layout(barmode='group')
            
    return fig


def clean_code(df1):
    """ This function are cleaning out dataset
        Cleaning types:
        1. Remove NaN obs;
        2. Column type change
        3. Remove blank on the variables names
        4. Convert to timedate variable
        5. Clean variable time    
        
        Input: Dataframe
        Output: Dataframe
    
    """
    
    # 0. Removing missing values
    fighas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[fighas_selecionadas, :].copy()

    fighas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[fighas_selecionadas, :].copy()

    fighas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[fighas_selecionadas, :].copy()

    fighas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[fighas_selecionadas, :].copy()

    # 1. Converting Age column from text to int
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)


    # 2. Converting Rating column from text to float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 3. Converting order_date column from text to date
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

    #4. Converting multiple_deliveries column from text to int
    fighas_selecionadas = (df1['multiple_deliveries']!= 'NaN ')
    df1 = df1.loc[fighas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #5. Removing blank spaces in strings/text/objects (another way to do it)
    df1.loc[:, 'ID'] = df1.loc[:,'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    #6. Cleaning Time taken column
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1

# ================== Code's logical structure ======================== #

# ==========================
#Import Dataset
# ==========================
df = pd.read_csv('train.csv')

# Cleaning data
df1 = clean_code(df)


# =======================================
#        SideBar --   Streamlit
# =======================================

# Image
image = Image.open('jnts.jpg')
st.sidebar.image(image, width=120)

#SIDEBAR

st.header('Marketplace - Restaurant Overview')
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Please select the limit date')

date_slider = st.sidebar.slider(
    'Which Value?',
    value = pd.datetime(2022, 4, 13),
    min_value = pd.datetime(2022, 2, 11),
    max_value = pd.datetime(2022, 4, 6),
    format='DD-MM-YYYY' )

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Which are traffic conditions?',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam']) 

st.sidebar.markdown("""---""")

weather_options = st.sidebar.multiselect(
    'Which are weather conditions?',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorm', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default = ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorm', 'conditions Stormy', 'conditions Sunny', 'conditions Windy']) 
st.sidebar.markdown("## Powered by Jonatas Vieira, MSc.")

### FILTERS

### Date filter

selected_rows = df1['Order_Date'] < date_slider
df1 = df1.loc[selected_rows, :]

### Traffic filter
selected_rows = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[selected_rows, :]

### Weather filter
selected_rows = df1['Weatherconditions'].isin(weather_options)
df1 = df1.loc[selected_rows, :]

# =======================================
#      Streamlit -- Layout
# =======================================
tab1, tab2, tab3 = st.tabs(['Management View', '', ''])

with tab1:
    with st.container():
        st.title("Overall Metrics")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Unique delivery person', delivery_unique)
            
        with col2:
            avg_distance = distance(df1)
            col2.metric('Avg delivery distance', avg_distance)
     
        with col3:
            aux = avg_std_time_delivery(df1, 'Yes','avg_time')
            col3.metric('Average Time', aux)

        with col4:
            aux = avg_std_time_delivery(df1, 'Yes','std_time')
            col4.metric('Std delivery time', aux)
                   
        with col5:
            aux = avg_std_time_delivery(df1, 'No','avg_time')
            col5.metric('Avg delivery time', aux)
      
        with col6:
            aux = avg_std_time_delivery(df1, 'No','std_time')
            col6.metric('Std delivery time', aux) 
            
 ######## =================PIZZA================================

    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig)
        
        with col2:
            aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                      .groupby(['City', 'Type_of_order'])
                      .agg({'Time_taken(min)':['mean','std']}))

            aux.columns = ['avg_time', 'std_time']
            aux = aux.reset_index()
        
            st.dataframe(aux)

            
######## ===========================================================

    with st.container():
        st.markdown("""---""")
        st.title("Time distribution")
        
        col1, col2 = st.columns(2)
        with col1:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']

            df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)

            avg_distance = df1.loc[:,['City', 'distance']].groupby('City').mean().reset_index()

            fig = go.Figure(data = [go.Pie(labels=avg_distance['City'], values = avg_distance['distance'], pull=[0, 0.1,0])])
            st.plotly_chart(fig)
        
            
        with col2:
            df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                          .groupby(['City', 'Road_traffic_density'])
                          .agg({'Time_taken(min)': ['mean', 'std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig = px.sunburst(df_aux, path = ['City', 'Road_traffic_density'], values = 'avg_time',
                             color = 'std_time', color_continuous_scale='RdBu',
                             color_continuous_midpoint=np.average(df_aux['std_time']))
            st.plotly_chart(fig)

        
