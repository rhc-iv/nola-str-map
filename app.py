# Import statements:
import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import folium_static

# API Endpoint/API Token variables:
API_ENDPOINT = 'https://data.nola.gov/resource/rbhq-zbz9.json'
API_TOKEN = 'arcj5VhkiIB7k52gDpNQXiENV'

# Make the call to the API:
response = requests.get(API_ENDPOINT + '?$$app_token=' + API_TOKEN)
data = response.json()

# Form the API response into a Pandas DataFrame:
df = pd.DataFrame(data)

# Set the 'Type' field to specific values:
df = df.loc[df['type'].isin(['Short Term Rental Residential Owner',
                             'Short Term Rental Commercial Owner'])]

# Keep only the desired columns in the DataFrame:
df = df.loc[:,
     ['address', 'type', 'bedroom_limit', 'guest_limit', 'expiration_date',
      'x', 'y']]

# Rename specific columns in the DataFrame:
df = df.rename(columns={
    'bedroom_limit'  : 'Bedroom limit',
    'guest_limit'    : 'Guest limit',
    'expiration_date': 'Expiration date',
    'x'              : 'Latitude',
    'y'              : 'Longitude'
})

# Capitalize the DataFrame column names:
df.columns = df.columns.str.capitalize()

# Define and create the Streamlit sidebar menus:
st.sidebar.header('Filter Data')
filter_address = st.sidebar.selectbox(
    'Address',
    [''] + list(df['Address'].unique()),
    index=0
)
filter_type = st.sidebar.selectbox(
    'Type',
    [''] + list(df['Type'].unique()),
    index=0
)
filter_bedroom = st.sidebar.selectbox(
    'Bedroom Limit',
    [''] + list(df['Bedroom limit'].unique()),
    index=0
)
filter_guest = st.sidebar.selectbox(
    'Guest Limit',
    [''] + list(df['Guest limit'].unique()),
    index=0
)
filter_exp = st.sidebar.selectbox(
    'Expiration Date',
    [''] + list(df['Expiration date'].unique()),
    index=0
)

# Define the Clear/Submit buttons:
submit_button = st.sidebar.button('Submit')
clear_button = st.sidebar.button('Clear')

# Filter the Dataframe based on user selection/Submit button activation:
if submit_button:
    filtered_df = df.loc[
        (df['Address'] == filter_address) &
        (df['Type'] == filter_type) &
        (df['Bedroom limit'].isin([filter_bedroom])) &
        (df['Guest limit'].isin([filter_guest])) &
        (df['Expiration date'].isin([filter_exp]))
        ]
    # Convert the filtered DataFrame into an HTML table;
    table = filtered_df.to_html(index=False)

    # Plot the selected address on a map in the Streamlit window:
    if not filtered_df.empty:
        lat = filtered_df.iloc[0]['Latitude']
        long = filtered_df.iloc[0]['Longitude']
        map_filtered = folium.Map(
            location=[lat, long],
            zoom_start=15
        )
        folium.Marker(
            location=[lat, long],
            popup=filter_address
        ).add_to(map_filtered)
        # Display the map for the filtered address in the Streamlit window:
        folium_static(map_filtered)

        # Only plot the selected address on a map after the user has
        # submitted the filter form:
        if submit_button:
            if not filtered_df.empty:
                lat = filtered_df.iloc[0]['Latitude']
                long = filtered_df.iloc[0]['Longitude']
                map_filtered = folium.Map(
                    location=[lat, long],
                    zoom_start=15
                )
                folium.Marker(
                    location=[lat, long],
                    popup=filter_address
                ).add_to(map_filtered)
                # Display the map for the filtered address in the Streamlit window:
                folium_static(map_filtered)

    # Plot all of the addresses on a map in the Streamlit window:
    map_all = folium.Map(location=[29.95, -90.07], zoom_start=14)

    # Define marker icon colors based on the selected type
    icon_color = {'Short Term Rental Commercial Owner' : 'blue',
                  'Short Term Rental Residential Owner': 'green'}

    for _, row in df.iterrows():
        marker_color = icon_color.get(row['Type'], 'red')
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Address'],
            icon=folium.Icon(color=marker_color)
        ).add_to(map_all)

    # Display the map for all addresses in the Streamlit window:
    folium_static(map_all)

    # Only plot the selected address on a map after the user has
    # submitted the filter form:
    if submit_button:
        if not filtered_df.empty:
            lat = filtered_df.iloc[0]['Latitude']
            long = filtered_df.iloc[0]['Longitude']
            # Define marker icon color based on the selected type
            marker_color = icon_color.get(filtered_df.iloc[0]['Type'], 'red')
            map_filtered = folium.Map(
                location=[lat, long],
                zoom_start=15
            )
            folium.Marker(
                location=[lat, long],
                popup=filter_address,
                icon=folium.Icon(color=marker_color)
            ).add_to(map_filtered)
            # Display the map for the filtered address in the Streamlit window:
            folium_static(map_filtered)

