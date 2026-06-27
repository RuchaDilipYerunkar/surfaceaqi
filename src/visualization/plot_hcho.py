import os
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# 1. Define folder paths matching your repository structure
tif_path = os.path.join("data", "raw", "hcho_india_may2026.tif")
output_png = os.path.join("outputs", "figures", "hcho_india_visualization.png")

if not os.path.exists(tif_path):
    print(f"Error: Missing file at {tif_path}")
    print("Please ensure you downloaded 'hcho_india_may2026.tif' from Drive and put it in data/raw/")
    exit()

# 2. Open and read the satellite raster layers
with rasterio.open(tif_path) as src:
    print("\n==================================================")
    print("SUCCESS: Satellite GeoTIFF Opened Successfully!")
    print(f"Image Resolution: {src.width} x {src.height}")
    print(f"Coordinate Reference System: {src.crs}")
    print("==================================================\n")
    
    # 3. Setup the matplotlib map frame
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 4. Render the map array using a vibrant palette to emphasize high concentrations
    image_plot = show(src, ax=ax, cmap="inferno", title="Sentinel-5P HCHO Hotspot Mapping over India (May 2026)")
    
    # 5. Export high-resolution PNG artifact
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"Success: High-resolution PNG saved to: {output_png}")
    plt.show()