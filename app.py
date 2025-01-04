import streamlit as st
import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Title and description
st.title("SPI Drought Monitoring Map")
st.write("""
This application displays the Standardized Precipitation Index (SPI) map for drought monitoring. 
The SPI is categorized into various drought levels, as follows:
""")

# Add legend description
st.markdown("""
- **Red**: Extreme drought (< -2.00)
- **Orange**: Severe drought (-1.99 to -1.50)
- **Yellow**: Moderate drought (-1.49 to -1.00)
- **White**: Mild drought (-0.99 to 0.00)
- **Blue**: No drought (> 0.00)
""")

# Load the GeoTIFF file
file_path = "./data/SPI_2023.tif"

try:
    with rasterio.open(file_path) as src:
        spi_data = src.read(1)  # Read the first band
        spi_transform = src.transform

    # Replace invalid values (like -9999) with NaN for better visualization
    spi_data = np.where(spi_data == src.nodata, np.nan, spi_data)

    # Define a custom color map
    from matplotlib.colors import ListedColormap
    colors = ['red', '#FF8000', '#FFFF00', '#FFFFFF', 'blue']
    cmap = ListedColormap(colors)

    # Define SPI thresholds
    bounds = [-np.inf, -2.00, -1.50, -1.00, 0.00, np.inf]
    norm = plt.Normalize(vmin=-2.00, vmax=2.00)

    # Plot the map
    fig, ax = plt.subplots(figsize=(8, 8))
    cax = ax.imshow(spi_data, cmap=cmap, norm=norm)
    ax.set_title("SPI Map (2023)")
    plt.colorbar(cax, ax=ax, orientation="vertical", ticks=bounds, label="SPI Levels")

    # Display the map in Streamlit
    st.pyplot(fig)

except FileNotFoundError:
    st.error("The SPI GeoTIFF file was not found. Please ensure it is located in the `data` directory.")




