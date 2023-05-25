import scipy.spatial
import XmlToGrid
import cv2
import numpy as np

grid = XmlToGrid.ShakeMapGrid()
grid.load("us20005j32.xml")
print(len(grid.grid))
print(grid.grid[0]["LON"])








# Read the tif file
image = cv2.imread('countriesISOraster.tif')
print(len(image))

range_of_lon=np.arange(-180.0000,179.999986,0.0083334)
range_of_lat=np.arange(83.6333,-90.0000,-0.0083334)

print("lat then lon range:", len(range_of_lat), len(range_of_lon))

lat_vals = [grid.lat_min,grid.lat_max, grid.lat]
lon_vals = [grid.lon_min,grid.lon_max, grid.lon]

lat_corner=[grid.lat_min,grid.lat_max,grid.lat_min,grid.lat_max]
lon_corner=[grid.lon_max,grid.lon_max,grid.lon_min,grid.lon_min]
corners = [lat_corner, lon_corner]
print(corners)
col = []
row = []

for x in lat_vals:
    curr_idx = ((np.abs(range_of_lat - x)).argmin())
    row.append(curr_idx)

for x in lon_vals:
    curr_idx = ((np.abs(range_of_lon - x)).argmin())
    col.append(curr_idx)
print("cols: ", col)
print("rows: ", row)

print(grid.lon)#how to get epicenter
print(grid.lat)#how to get epicenter


print(grid.lat_max)#coorners
print(grid.lat_min)#