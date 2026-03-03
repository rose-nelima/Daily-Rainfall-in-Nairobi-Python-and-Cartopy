import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys
import geopandas as gpd
import cartopy.feature as cfeature

if len(sys.argv) < 2:
    print("Usage: python rainfall_map_nc.py yourfile.nc")
    sys.exit(1)

filename = sys.argv[1]
ds = xr.open_dataset(filename, engine="netcdf4")
print(ds)

# --- 1. Load NetCDF rainfall data ---
#ds = xr.open_dataset("chirps.nc")  # or your WRF file

# Pick rainfall variable (adjust for WRF if needed)
rain = ds[list(ds.data_vars)[0]]    # first variable
rain_day = rain[0]                  # first timestep
lat = ds["latitude"]
lon = ds["longitude"]

# --- 2. Find Nairobi region indices ---
# Approximate Nairobi bounding box
lat_min, lat_max = -1.5, -1.0
lon_min, lon_max = 36.7, 37.0

# Mask rainfall outside Nairobi
rain_nairobi = rain_day.where(
    (lat >= lat_min) & (lat <= lat_max) &
    (lon >= lon_min) & (lon <= lon_max)
)

# --- 3. Categorize rainfall ---
rain_cat = np.zeros_like(rain_nairobi)
rain_cat[(rain_nairobi>0) & (rain_nairobi<=5)] = 1
rain_cat[(rain_nairobi>5) & (rain_nairobi<=20)] = 2
rain_cat[(rain_nairobi>20) & (rain_nairobi<=50)] = 3
rain_cat[rain_nairobi>50] = 4

cmap = plt.cm.Blues
bounds = [0,1,2,3,4,5]
labels = ["No rain","Light","Moderate","Heavy","Very Heavy"]

# --- 4. Create map for Nairobi ---
plt.figure(figsize=(8,8))
ax = plt.axes(projection=ccrs.PlateCarree())

cf = ax.contourf(lon, lat, rain_cat, levels=bounds, cmap=cmap, extend='max')

# Add map features
ax.coastlines(resolution='10m')
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.RIVERS)

# Zoom to Nairobi
ax.set_extent([lon_min, lon_max, lat_min, lat_max])

# Mark Nairobi city center
ax.plot(36.8219, -1.2921, 'ro', markersize=6)
ax.text(36.83, -1.29, "Nairobi", fontsize=10)

# Add legend / colorbar
cbar = plt.colorbar(cf, ticks=[0.5,1.5,2.5,3.5,4.5])
cbar.ax.set_yticklabels(labels)
cbar.set_label("Rainfall Intensity")

# Map title and description
plt.title("Daily Rainfall in Nairobi", fontsize=14)
plt.text(36.7, -1.48, "Blue shades show rainfall intensity:\nLight → Moderate → Heavy → Very Heavy", 
         fontsize=10, bbox=dict(facecolor='white', alpha=0.6))

plt.show()

