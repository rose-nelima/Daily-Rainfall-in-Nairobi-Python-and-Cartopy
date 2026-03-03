# Nairobi Rainfall Intensity Mapper

**Visualizes daily rainfall data from NetCDF files, generating categorized intensity maps focused on Nairobi, Kenya.**

 

## 🎯 Purpose
Maps rainfall intensity across Nairobi using CHIRPS or WRF NetCDF data, categorizing precipitation into No Rain/Light/Moderate/Heavy/Very Heavy classes for meteorological analysis and urban planning.

## ✨ Features
- Processes `.nc` NetCDF files (CHIRPS, WRF compatible)
- Crops to Nairobi bounding box (lat: -1.5° to -1.0°, lon: 36.7° to 37.0°)
- 4-tier rainfall categorization based on mm/day thresholds
- Professional cartographic visualization with coastlines, borders, rivers
- Nairobi city center marker with custom colorbar legend

## 📦 Prerequisites
```bash
pip install xarray netcdf4 matplotlib cartopy geopandas numpy

## 📦 Usage
```bash
python rainfall_map_nc.py your_rainfall_file.nc


