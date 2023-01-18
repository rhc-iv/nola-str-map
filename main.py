#!/usr/bin/env python3

import pandas as pd
import tkinter
from geopy.geocoders import Nominatim
from tkintermapview import TkinterMapView

# Read CSV file
df = pd.read_csv("nola_str_001.csv")

# Create an empty list to store the GPS coordinates
coordinates = []

# Use geopy to convert addresses to GPS coordinates
geolocator = Nominatim(
    timeout=10,
    user_agent="PFD")
for address in df["Address"]:
    location = geolocator.geocode(address)
    if location:
        coordinates.append((location.latitude, location.longitude))

# Create a Tkinter map view:
root_tk = tkinter.Tk()
root_tk.geometry(f"{3024}x{1964}")
root_tk.title("NOLA Short-Term Rentals.py")

map_widget = TkinterMapView(
    root_tk,
    width=3000,
    height=1900,
    corner_radius=0,
)
map_widget.place(
    relx=0.5,
    rely=0.5,
    anchor=tkinter.CENTER
)
# Set current widget position and zoom:
map_widget.set_position(29.951065, -90.071533)  # New Orleans
map_widget.set_zoom(15)

# Add markers for each GPS coordinate to the map
for coord in coordinates:
    map_widget.set_marker(
        deg_x=coord[0],
        deg_y=coord[1],
    )

# Display the map
map_widget.mainloop()
