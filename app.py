import streamlit as st
import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from rasterio.plot import show

# Set up page configuration
st.set_page_config(page_title="Drought Monitoring", layout="wide")

# Load GeoTIFF data
def load_tif(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)
        return data, src.transform

# Display title
st.title("Drought Monitoring Application")

# Add a description
st.write("""
This application visualizes and analyzes drought conditions in the Arbil region.
It uses the SPI, NDVI, and SMAP datasets to provide insights into vegetation health and soil moisture.
""")

# Load and display NDVI data
st.header("NDVI Data (Vegetation Health)")
ndvi_data, _ = load_tif('data/NDVI_Arbil.tif')
st.image(ndvi_data, caption="NDVI Map", use_column_width=True)

# Load and display SPI data
st.header("SPI Data (Drought Index)")
spi_data, _ = load_tif('data/SPI_12_Month_2023.tif')
st.image(spi_data, caption="SPI Map", use_column_width=True)

# Load and display SMAP data
st.header("SMAP Data (Soil Moisture)")
smap_data, _ = load_tif('data/SMAP_2023_GeoTIFF (1).tif')
st.image(smap_data, caption="SMAP Map", use_column_width=True)

# Additional analysis or plots can go here
st.header("Drought Severity")
# Example of drought severity analysis based on SPI thresholds
thresholds = {
    'Extreme drought': -2.0,
    'Severe drought': -1.5,
    'Moderate drought': -1.0,
    'Mild drought': 0.0
}
st.write(f"Thresholds: {thresholds}")



