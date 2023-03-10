# Libraries

import pandas as pd
import plotly.express as px
import folium
from haversine import haversine
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static

st.set_page_config(page_title= "Delivery View", page_icon = "🚚", layout='wide')

# ==========================
# Functions
# ==========================

def top_delivers(df1, top_asc):
    df2 = (df1.loc[:, ['Delivery_person_ID','City','Time_taken(min)']]
              .groupby(['City','Delivery_person_ID'])
              .mean()
              .sort_values(['City','Time_taken(min)'], ascending = top_asc)
              .reset_index())

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop = True)
    return df3

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
df = pd.read_csv('dataset/train.csv')

# Cleaning data
df1 = clean_code(df)


# =======================================
#        SideBar --   Streamlit
# =======================================

# Image
image = Image.open('jnts.jpg')
st.sidebar.image(image, width=120)

#SIDEBAR

st.header('Marketplace - Customer Overview')
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
        st.title('Overall Delivery Metrics')
        
        col1, col2, col3, col4 = st.columns(4, gap = 'large')
        with col1:
            st.subheader('Older Delivery Person')
            oldest = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Oldest', oldest)

        
        with col2:
            st.subheader('Younger Delivery Person')
            young = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Younger', young )
        
        with col3:
            st.subheader('Best vehicle condition')
            best = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Best condition', best )
            
        with col4:
            st.subheader('Worse vehicle condition')
            worse = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Worse condition', worse )
            
    with st.container():
        st.markdown("""---""")
        st.title('Ratings')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Average rating per delivery man')
            df_avg_ratings_per_deliver = (df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID')
                    .mean()
                    .reset_index())
            st.dataframe(df_avg_ratings_per_deliver)
            
        with col2:
            st.markdown('##### Average rating per traffic')
            df_avg_std_rating_by_traffic = (df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density')
                                                   .agg({'Delivery_person_Ratings': ['mean','std']}))
            
            #change cols name
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']
            #reseting index
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            
            st.dataframe(df_avg_std_rating_by_traffic)

           
            st.markdown('##### Average rating per weather')
            # using .agg function
            df_avg_std_rating_by_weather = (df1.loc[:, ['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions')
                                                .agg({'Delivery_person_Ratings': ['mean','std']}))
            #change cols name
            df_avg_std_rating_by_weather.columns = ['delivery_mean', 'delivery_std']
            #reseting index
            df_avg_std_rating_by_weather = df_avg_std_rating_by_weather.reset_index()
            st.dataframe(df_avg_std_rating_by_weather)
        
    with st.container():
        st.markdown("""---""")
        st.title('Delivery Speed')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Fastest delivery guys')
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)
            
            
        with col2:
            st.markdown('##### Slowest delivery person')
            df3 = top_delivers(df1, top_asc=False)
            st.dataframe(df3)
            
