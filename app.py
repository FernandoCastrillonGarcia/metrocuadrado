import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from utils2 import html_creator, create_map

# Function to generate a DataFrame (dummy function for illustration)
def process_text(text):
    # Process the text through a ML model to get data (example data here)
    data = {'Input Text': [text], 'Processed Result': ['Result of processing']}
    return pd.DataFrame(data)

df = pd.read_pickle('data/geoProperties.pkl')
# Streamlit application layout
st.title('ML Text Processing Application')

# Text input
user_input = st.text_area("Enter text here:", "Type Here")

# Processing button
if st.button('Process'):
    # Display DataFrame
    result_df = process_text(user_input)
    st.write(result_df)

    # Display Folium map
    st.subheader('Folium Map')
    st_folium_map = create_map(df)
    folium_static(st_folium_map)
