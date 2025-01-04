import streamlit as st
import geopandas as gpd
import rasterio
import folium
from rasterio.mask import mask
from folium.raster_layers import ImageOverlay
import numpy as np
from matplotlib import cm
from streamlit_folium import st_folium

# Title and description
st.title("SPI Drought Monitoring Map")
st.write("""
This application displays the Standardized Precipitation Index (SPI) map for drought monitoring.
The SPI is categorized into various drought levels:
""")

# Add legend description
st.markdown("""
- **Red**: Extreme drought (< -2.00)
- **Orange**: Severe drought (-1.99 to -1.50)
- **Yellow**: Moderate drought (-1.49 to -1.00)
- **White**: Mild drought (-0.99 to 0.00)
- **Blue**: No drought (> 0.00)
""")

# File path to the GeoTIFF
file_path = "./data/SPI_2023.tif"

# Load GeoTIFF and process data
try:
    with rasterio.open(file_path) as src:
        spi_data = src.read(1)  # Read the first band
        spi_transform = src.transform
        spi_bounds = src.bounds
        spi_crs = src.crs

    # Replace invalid values (like -9999) with NaN
    spi_data = np.where(spi_data == src.nodata, np.nan, spi_data)

    # Normalize SPI data for color mapping
    spi_min, spi_max = -2, 2
    spi_data_normalized = np.clip((spi_data - spi_min) / (spi_max - spi_min), 0, 1)

    # Define color mapping
    cmap = cm.get_cmap("RdYlBu", 5)  # Red to Blue color map with 5 categories
    colormap = cm.ScalarMappable(cmap=cmap)

    # Create Folium Map
    map_center = [(spi_bounds.top + spi_bounds.bottom) / 2, (spi_bounds.left + spi_bounds.right) / 2]
    m = folium.Map(location=map_center, zoom_start=8, tiles="cartodbpositron")

    # Overlay GeoTIFF data
    def create_colormap(value):
        if value < -2:
            return "red"
        elif -1.99 <= value <= -1.50:
            return "orange"
        elif -1.49 <= value <= -1.00:
            return "yellow"
        elif -0.99 <= value <= 0.00:
            return "white"
        else:
            return "blue"

    overlay_image = np.array([[create_colormap(val) for val in row] for row in spi_data])

    folium.raster_layers.ImageOverlay(
        image=overlay_image,
        bounds=[[spi_bounds.bottom, spi_bounds.left], [spi_bounds.top, spi_bounds.right]],
        opacity=0.6
    ).add_to(m)

    # Add a legend
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 150px; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; padding: 10px;">
    <b>SPI Legend:</b><br>
    <i style="background: red; width: 15px; height: 15px; float: left; margin-right: 5px;"></i>Extreme drought (< -2.00)<br>
    <i style="background: orange; width: 15px; height: 15px; float: left; margin-right: 5px;"></i>Severe drought (-1.99 to -1.50)<br>
    <i style="background: yellow; width: 15px; height: 15px; float: left; margin-right: 5px;"></i>Moderate drought (-1.49 to -1.00)<br>
    <i style="background: white; width: 15px; height: 15px; float: left; margin-right: 5px;"></i>Mild drought (-0.99 to 0.00)<br>
    <i style="background: blue; width: 15px; height: 15px; float: left; margin-right: 5px;"></i>No drought (> 0.00)<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display the map in Streamlit
    st.write("### Interactive SPI Map")
    st_folium(m, width=700, height=500)

except FileNotFoundError:
    st.error("The SPI GeoTIFF file was not found. Please ensure it is located in the `data` directory.")

