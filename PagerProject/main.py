import PIL
import scipy.spatial
import XmlToGrid
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import Opening_files
import os

'''
Task 1: Getting the xml file to grid
'''
grid = XmlToGrid.ShakeMapGrid()
grid.load("us20005j32.xml")
#print(len(grid.grid))
#print(grid.grid[0]["LON"])

'''
Task 2: Getting tif file read to get country codes
'''

# Open the TIFF file
PIL.Image.MAX_IMAGE_PIXELS = 900115200
img = Image.open('countriesISOraster.tif')
img_arr = np.array(img)

'''
Task 3: Getting the country code
'''

#print(grid.lon) # how to get epicenter
#print(grid.lat) # how to get epicenter
#print(grid.lat_max) # corners
#print(grid.lat_min)

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

#Country codes
ccode = list(img_arr[row,col])
ccode.sort()
#print("country codes: ", ccode)
#print("cols: ", col)
#print("rows: ", row)

# replace duplicate US codes
'''
ccode.replace(904,903)
ccode = np.where(ccode == 903, 902, ccode)
ccode = np.where(ccode == 904, 902, ccode)
print("replacing", ccode)
'''
ccode = list(set(ccode))
#print("unique", ccode)

'''
Task 4: Reading in files
'''

globalstructvuln = pd.read_csv("expo_data/struct_vulnerability.csv")
globalnonstructvuln=pd.read_csv("expo_data/nonstruct_vulnerability.csv")
globalcontentsvuln=pd.read_csv("expo_data/contents_vulnerability.csv")
globalstructfrag=pd.read_csv("expo_data/struct_fragility.csv")

ccode = [218] # country code for Ecuador, the only country of ccode we have the files for
for country in ccode:
    if(country == 0):
        continue
    ccode_files, country_name = Opening_files.read_files(country) # get list of filenames and country name
    
    expo_files_name= os.listdir('expo_data') # get list of files in expo_data folder
    
    # structural vulnerability
    if ccode_files[3] in expo_files_name:
        contrystructvuln= pd.read_csv("expo_data/" + ccode_files[3])
    elif ccode_files[4] in expo_files_name:
        contrystructvuln= pd.read_csv("expo_data/" + ccode_files[4])
    else:
        countrystructvuln = 0
        print('there is no country or region specific structural vulnerability file for this country')
    # nonstructural vulnerability
    if ccode_files[5] in expo_files_name:
        contrynonstructvuln= pd.read_csv("expo_data/" + ccode_files[5])
    elif ccode_files[6] in expo_files_name:
        contrynonstructvuln= pd.read_csv("expo_data/" + ccode_files[6])
    else:
        countrynonstructvuln = 0
        print('there is no country or region specific nonstructural vulnerability file for this country')
    # contents vulnerability
    if ccode_files[7] in expo_files_name:
        contrycontentsvuln= pd.read_csv("expo_data/" + ccode_files[7])
    elif ccode_files[8] in expo_files_name:
        contrycontentsvuln= pd.read_csv("expo_data/" + ccode_files[8])
    else:
        countrycontentsvuln = 0
        print('there is no country or region specific contents vulnerability file for this country')
    # taxonomy mapping
    if str(ccode_files[9]) in expo_files_name:
        taxonomymapping= pd.read_csv("expo_data/" + ccode_files[9])
    elif ccode_files[10] in expo_files_name:
        taxonomymapping= pd.read_csv("expo_data/" + ccode_files[10])
    else:
        taxonomymapping = 0
        print('taxonomy mapping file is missing for this country')
        break
    
    # read in exposure files
    ExposureRes=pd.read_csv("expo_data/" + ccode_files[1])
    ExposureCom=pd.read_csv("expo_data/" + ccode_files[2])
    ExposureCom=pd.read_csv("expo_data/" + ccode_files[3])








    #print(ccode_files, country)

