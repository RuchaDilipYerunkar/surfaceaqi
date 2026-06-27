import ee

# 1. Initialize Earth Engine with your whitelisted project ID
try:
    ee.Initialize(project='isro-aqi-hcho')
    print("Handshake Complete: Connected to Earth Engine servers.")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

# 2. Load India's Boundary Shape (FeatureCollection)
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
india_boundary = countries.filter(ee.Filter.eq('country_na', 'India'))

# 3. Load Sentinel-5P HCHO Offline Dataset (ImageCollection)
# Corrected band name based on catalog guidelines: 'tropospheric_HCHO_column_number_density'
hcho_collection = (
    ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_HCHO")
    .select("tropospheric_HCHO_column_number_density")
    .filterDate("2026-05-01", "2026-05-31")  # Filtering for May 2026 data
    .filterBounds(india_boundary)
)

print(f"Total satellite images found in collection window: {hcho_collection.size().getInfo()}")

# 4. Compute Temporal Average & Clip to India Border
hcho_mean = hcho_collection.mean()
hcho_india = hcho_mean.clip(india_boundary)

# 5. Define an Asynchronous Cloud Export Task to Google Drive
print("Setting up cloud export parameters...")
export_task = ee.batch.Export.image.toDrive(
    image=hcho_india,
    description="Sentinel5P_HCHO_India_May2026",
    folder="GEE_Outputs",                  # Folder that will be created in your Google Drive
    fileNamePrefix="hcho_india_may2026",
    scale=1113.2,                          # Resolution scale matching native TROPOMI (~1.1 km)
    region=india_boundary.geometry(),     # Geometry boundary to crop by
    maxPixels=1e9
)

# Start execution on the Google Cloud side
export_task.start()

print("\n==================================================")
print("SUCCESS: Data processing script executed locally!")
print(f"Cloud Export Task Status: {export_task.status()['state']}")
print(f"Task ID: {export_task.id}")
print("==================================================")
print("You can check your Google Drive 'GEE_Outputs' folder shortly for the completed GeoTIFF.")