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
    spi_data_clipped = np.clip(spi_data, spi_min, spi_max)

    # Define color mapping using Matplotlib's colormap
    cmap = cm.get_cmap("RdYlBu", 5)  # Red to Blue color map with 5 categories
    norm = cm.colors.Normalize(vmin=spi_min, vmax=spi_max)
    spi_colormap = cm.ScalarMappable(norm=norm, cmap=cmap)

    # Convert SPI data to an RGB image for overlay
    spi_rgb = spi_colormap.to_rgba(spi_data_clipped, bytes=True)[:, :, :3]

    # Create Folium Map
    map_center = [(spi_bounds.top + spi_bounds.bottom) / 2, (spi_bounds.left + spi_bounds.right) / 2]
    m = folium.Map(location=map_center, zoom_start=8, tiles="cartodbpositron")

    # Overlay GeoTIFF data
    bounds = [[spi_bounds.bottom, spi_bounds.left], [spi_bounds.top, spi_bounds.right]]
    folium.raster_layers.ImageOverlay(
        image=spi_rgb,
        bounds=bounds,
        opacity=0.6
    ).add_to(m)

    # Add a legend
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 250px; height: 180px; 
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; padding: 10px;">
    <b>SPI Legend:</b><br>
    <i style="background: red; width: 15px; height: 15px; display: inline-block;"></i> Extreme drought (< -2.00)<br>
    <i style="background: orange; width: 15px; height: 15px; display: inline-block;"></i> Severe drought (-1.99 to -1.50)<br>
    <i style="background: yellow; width: 15px; height: 15px; display: inline-block;"></i> Moderate drought (-1.49 to -1.00)<br>
    <i style="background: white; width: 15px; height: 15px; display: inline-block; border:1px solid grey;"></i> Mild drought (-0.99 to 0.00)<br>
    <i style="background: blue; width: 15px; height: 15px; display: inline-block;"></i> No drought (> 0.00)<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display the map in Streamlit
    st.write("### Interactive SPI Map")
    st_folium(m, width=700, height=500)

except FileNotFoundError:
    st.error("The SPI GeoTIFF file was not found. Please ensure it is located in the `data` directory.")
except Exception as e:
    st.error(f"An error occurred: {e}")

