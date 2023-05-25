import scipy.spatial
import XmlToGrid
import cv2
import numpy as np
import PIL
from PIL import Image

grid = XmlToGrid.ShakeMapGrid()
grid.load("us20005j32.xml")


# Read the tif file
PIL.Image.MAX_IMAGE_PIXELS = 900115200
img = Image.open('countriesISOraster.tif')
img_arr = np.array(img)

range_of_lon=np.arange(-180.0000,179.999986,0.0083334)
range_of_lat=np.arange(83.6333,-90.0000,-0.0083334)

lon_vals=[grid.lon_min,grid.lon_max,grid.lon_min,grid.lon_max, grid.lon]
lat_vals=[grid.lat_max,grid.lat_max,grid.lat_min,grid.lat_min, grid.lat]
col = []
row = []

for x in lon_vals:
    curr_idx = ((np.abs(range_of_lon - x)).argmin())
    col.append(curr_idx)

for x in lat_vals:
    curr_idx = ((np.abs(range_of_lat - x)).argmin())
    row.append(curr_idx)


corners = [row, col]
print(corners)
ccode = img_arr[row,col]
print(ccode)


Reading in files
'''
globalstructvuln = pd.read_csv("expo_data/struct_vulnerability.csv")
globalnonstructvuln=pd.read_csv("expo_data/nonstruct_vulnerability.csv")
globalcontentsvuln=pd.read_csv("expo_data/contents_vulnerability.csv")
globalstructfrag=pd.read_csv("expo_data/struct_fragility.csv")
