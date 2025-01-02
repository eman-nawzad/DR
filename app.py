import streamlit as st
import rasterio
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
    with rasterio.open(file_path) as src:
        st.write(f"File CRS: {src.crs}")
        st.write(f"Bounds: {src.bounds}")
        data = src.read(1)  # Reading the first band
        st.write(f"Shape: {data.shape}")
        st.image(data, caption=f"{dataset_option} Visualization", use_column_width=True)
except rasterio.errors.RasterioIOError as rio_err:
    st.error(f"RasterioIOError: {rio_err}")
except Exception as e:
    st.error(f"Error loading dataset: {e}")

# Map visualization
if st.checkbox("Show on Map"):
    try:
        with rasterio.open(file_path) as src:
            bounds = src.bounds
            center_lat = (bounds.top + bounds.bottom) / 2
            center_lon = (bounds.left + bounds.right) / 2

            m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
            folium.Marker([center_lat, center_lon], popup=f"{dataset_option} Center").add_to(m)
            st.write(m._repr_html_(), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying map: {e}")

st.sidebar.info("Created by [Your GitHub Profile](https://github.com/eman-nawzad)")


