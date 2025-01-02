import streamlit as st
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
import folium

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
    # Read the GeoTIFF file using rioxarray
    data = rxr.open_rasterio(file_path, masked=True)

    # Extract data and metadata
    data_array = data[0]  # Use the first band
    bounds = data.rio.bounds()
    shape = data_array.shape

    st.write(f"Bounds: {bounds}")
    st.write(f"Shape: {shape}")
    st.image(data_array, caption=f"{dataset_option} Visualization", use_column_width=True)
except Exception as e:
    st.error(f"Error loading dataset: {e}")

# Map visualization
if st.checkbox("Show on Map"):
    try:
        bounds = data.rio.bounds()
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2

        # Create a Folium map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        folium.Marker([center_lat, center_lon], popup=f"{dataset_option} Center").add_to(m)

        # Display the map
        st.write(m._repr_html_(), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying map: {e}")

st.sidebar.info("Created by [Your GitHub Profile](https://github.com/eman-nawzad)")



