import streamlit as st
import rasterio
import geopandas as gpd
import folium
from folium.plugins import ColorMap

# Title and description
st.title("Drought Monitoring Application")
st.markdown("""
This application provides interactive visualization for analyzing:
- NDVI
- SMAP (Soil Moisture)
- SPI (Standardized Precipitation Index)
""")

# Dataset selection
st.sidebar.title("Dataset Options")
dataset_option = st.sidebar.selectbox("Choose a dataset:", ["NDVI", "SMAP", "SPI"])

# File paths
data_paths = {
    "NDVI": "data/NDVI_Arbil.tif",
    "SMAP": "data/SMAP_2023_GeoTIFF (1).tif",
    "SPI": "data/SPI_12_Month_2023.tif"
}

# Load and display dataset
file_path = data_paths[dataset_option]
st.write(f"Displaying dataset: {dataset_option}")

try:
    with rasterio.open(file_path) as src:
        bounds = src.bounds
        data = src.read(1)  # Reading the first band
        st.write(f"Bounds: {bounds}")
        st.write(f"Shape: {data.shape}")
        st.image(data, caption=f"{dataset_option} Visualization")
except Exception as e:
    st.error(f"Error loading dataset: {e}")

# Map visualization (optional)
if st.checkbox("Show on Map"):
    st.write("Map feature coming soon!")

st.sidebar.info("Created by [Your GitHub Profile](https://github.com/eman-nawzad)")

