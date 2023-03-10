import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🚃"
)


# image_path = "/Users/jonatas/Documents/repos/FTC/"
image = Image.open('jnts.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard was built to monitor growth metrics of delivery persons and Restaurants
    ### How to use this Dashboard?
    - Company Overview:
        - Management View: General growth metrics
        - Tatical View: Weekly growth parameters
        - Geographiv View: Geolovation insights
    - Delivery Overview:
        - Weekly performance growth rates
    - Restaurant Overview:
        - Weekly restaurants growth rates
    ### Ask for Help
        - MSc. Jonatas Vieira (@jntsvieira)
    """)
