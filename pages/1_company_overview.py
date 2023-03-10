# Libraries

import pandas as pd
import plotly.express as px
import folium
from haversine import haversine
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static

st.set_page_config(page_title= "Company View", page_icon = "📈", layout='wide')

# ==========================
# Functions
# ==========================
def order_metric(df1):
    cols=['ID','Order_Date']
    # row selection
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
            # plot fige graph
    fig = px.bar(df_aux, x = 'Order_Date', y= 'ID')
    return fig

def traffic_order_share(df1):
    df_aux = (df1.loc[:, ['ID','Road_traffic_density']]
               .groupby('Road_traffic_density')
               .count()
               .reset_index())
    df_aux = df_aux.loc[df_aux['Road_traffic_density']!= 'NaN', :]
    df_aux['entregas_perc'] = df_aux['ID']/df_aux['ID'].sum()
    # plotting pie graph
    pie = px.pie(df_aux, values='entregas_perc', names = 'Road_traffic_density')
    return pie

def traffic_order_city(df1):
    df_aux = (df1.loc[:,['ID','City','Road_traffic_density']]
                 .groupby(['City','Road_traffic_density'])
                 .count()
                 .reset_index())
    fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID')
    return fig

def order_by_week(df1):
    # creating a week column
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = (df1.loc[:, ['ID','week_of_year']]
                 .groupby('week_of_year')
                 .count()
                 .reset_index())
    #plot
    fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
    return fig

def order_share_by_week(df1):
    aux01 = (df1.loc[:, ['ID','week_of_year',]]
                .groupby('week_of_year')
                .count()
                .reset_index())
    aux02 = (df1.loc[:, ['Delivery_person_ID','week_of_year',]]
                 .groupby('week_of_year')
                 .nunique()
                 .reset_index())

    #using merge function
    aux = pd.merge(aux01, aux02, how = 'inner')
    aux['order_by_deliver'] = aux['ID']/aux['Delivery_person_ID']

    # plot
    fig = px.line(aux, x = 'week_of_year', y = 'order_by_deliver')
    return fig

def country_maps(df1):
    # using folium to draw the map
    df_aux = (df1.loc[:, ['City','Road_traffic_density', 'Delivery_location_latitude','Delivery_location_longitude']]
                 .groupby(['City', 'Road_traffic_density'])
                 .median()
                 .reset_index())

    map_ = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], 
                       location_info['Delivery_location_longitude']], 
                       popup = location_info[['City','Road_traffic_density']]).add_to(map_)


    folium_static(map_, width=1024, height = 600)

                

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
st.sidebar.image(image, width=100)

#SIDEBAR

st.header('Marketplace - Delivery Overview')
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
st.sidebar.markdown("## Powered by Jonatas Vieira, MSc.")

### FILTERS

### Date filter

selected_rows = df1['Order_Date'] < date_slider
df1 = df1.loc[selected_rows, :]

### Traffic filter
selected_rows = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[selected_rows, :]


# =======================================
#      Streamlit -- Layout
# =======================================
tab1, tab2, tab3 = st.tabs(['Management View', 'Tactical View', 'Geographic View'])

with tab1:
    with st.container():
        # Order Metric
        fig = order_metric(df1)
        st.markdown('# Orders by day')
        st.plotly_chart(fig, use_container_width = True)
        
        
    with st.container():
        col1, col2 = st.columns(2)
           
        with col1:
            fig = traffic_order_share(df1)
            st.markdown('## Traffic Order Share')   
            st.plotly_chart(fig, use_container_width = True)           
                               
        with col2:
            st.markdown('## Traffic Order City')
            fig = traffic_order_city(df1) 
            st.plotly_chart(fig, use_container_width = True)
            
                
        
with tab2:
    with st.container():
        st.markdown('## Order by week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, user_container_width = True)
        
    with st.container():
        st.markdown('## Order Share by week')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, user_container_width = True)
        
        
with tab3:
        st.markdown('## Country Maps')
        country_maps(df1)
        
