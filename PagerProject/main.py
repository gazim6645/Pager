import PIL
import scipy.spatial
import XmlToGrid
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import Opening_files
import getshakemapvalue
import os
import calcfunstructfrag
import calcfunstrucexp
import calcfunnonstrutcexp
import calcfuncontentsexp


import time
start_time = time.time()
'''
Task 1: Getting the xml file to grid
'''
grid = XmlToGrid.ShakeMapGrid()
grid.load("us20005j32.xml")
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
ccode = np.array(list(img_arr[row,col]))


# replace duplicate US codes, and get all unique codes
ccode[ccode == 903] = 902
ccode[ccode == 904] = 902
ccode = np.array(set(ccode))

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
    ExposureRes=pd.read_csv("expo_data/" + ccode_files[0]) #Only get the columns that are needed
    ExposureCom=pd.read_csv("expo_data/" + ccode_files[1])
    ExposureInd=pd.read_csv("expo_data/" + ccode_files[2])


    Sh_ExposureRes=getshakemapvalue.getshakemapvalue(grid, ExposureRes)
    Sh_ExposureCom=getshakemapvalue.getshakemapvalue(grid, ExposureCom)
    Sh_ExposureInd=getshakemapvalue.getshakemapvalue(grid, ExposureInd)


    #start fragility
    countrystructfrag=0.0
    struct_Res_damage,damage_states=calcfunstructfrag.calcfunstructfrag(Sh_ExposureRes, globalstructfrag, taxonomymapping,countrystructfrag)
    struct_Com_damage,damage_states=calcfunstructfrag.calcfunstructfrag(Sh_ExposureCom, globalstructfrag, taxonomymapping,countrystructfrag)
    struct_Ind_damage,damage_states=calcfunstructfrag.calcfunstructfrag(Sh_ExposureInd, globalstructfrag, taxonomymapping,countrystructfrag)

    slight_damage    = struct_Res_damage['slight'].sum() + struct_Com_damage['slight'].sum() + struct_Ind_damage['slight'].sum()
    moderate_damage  = struct_Res_damage['moderate'].sum() + struct_Com_damage['moderate'].sum() + struct_Ind_damage['moderate'].sum()
    extensive_damage = struct_Res_damage['extensive'].sum() + struct_Com_damage['extensive'].sum() + struct_Ind_damage['extensive'].sum()
    complete_damage  = struct_Res_damage['complete'].sum() + struct_Com_damage['complete'].sum() + struct_Ind_damage['complete'].sum()
    '''
    print('slight', slight_damage)
    print('moderate', moderate_damage)
    print('extensive', extensive_damage)
    print('complete', complete_damage)
    '''
    struct_Res= calcfunstrucexp.calcfunstrucexp(Sh_ExposureRes,globalstructvuln,taxonomymapping,countrystructvuln)
    struct_Com = calcfunstrucexp.calcfunstrucexp(Sh_ExposureCom,globalstructvuln,taxonomymapping,countrystructvuln)
    struct_Ind = calcfunstrucexp.calcfunstrucexp(Sh_ExposureInd,globalstructvuln,taxonomymapping,countrystructvuln)


    nonstruct_Res = calcfunnonstrutcexp.calcfunnonstrutcexp(Sh_ExposureRes,globalnonstructvuln,taxonomymapping,countrynonstructvuln)
    nonstruct_Com = calcfunnonstrutcexp.calcfunnonstrutcexp(Sh_ExposureCom,globalnonstructvuln,taxonomymapping,countrynonstructvuln)
    nonstruct_Ind = calcfunnonstrutcexp.calcfunnonstrutcexp(Sh_ExposureInd,globalnonstructvuln,taxonomymapping,countrynonstructvuln)



    contents_Res = calcfuncontentsexp.calcfuncontentsexp(Sh_ExposureRes,globalcontentsvuln,taxonomymapping,countrycontentsvuln)
    contents_Com = calcfuncontentsexp.calcfuncontentsexp(Sh_ExposureCom,globalcontentsvuln,taxonomymapping,countrycontentsvuln)
    contents_Ind = calcfuncontentsexp.calcfuncontentsexp(Sh_ExposureInd,globalcontentsvuln,taxonomymapping,countrycontentsvuln)


    Total_Structural_Loss=round((sum(struct_Res)+sum(struct_Com)+sum(struct_Ind))/1e6,2)
    Total_NonStructural_Loss=round((sum(nonstruct_Res)+sum(nonstruct_Com)+sum(nonstruct_Ind))/1e6,2)
    Total_Content_Loss=round((sum(contents_Res)+sum(contents_Com)+sum(contents_Ind))/1e6,2)

    loss=Total_Structural_Loss+Total_NonStructural_Loss+Total_Content_Loss

    print('Total eco. loss is', loss, 'Million USD for', country_name,'with struct_loss',Total_Structural_Loss, 'nonstruct_loss', Total_NonStructural_Loss, 'and content_loss', Total_Content_Loss)

    Sh_ExposureRes= Sh_ExposureRes.join(struct_Res_damage, how='right', sort=True)
    Sh_ExposureCom= Sh_ExposureCom.join(struct_Com_damage, how='right', sort=True)
    Sh_ExposureInd= Sh_ExposureInd.join(struct_Ind_damage, how='right', sort=True)

    nonstruct_Res=pd.DataFrame(np.array(nonstruct_Res),columns=["nonstruct_Res"])
    nonstruct_Com=pd.DataFrame(np.array(nonstruct_Com),columns=["nonstruct_Com"])
    nonstruct_Ind=pd.DataFrame(np.array(nonstruct_Ind),columns=["nonstruct_Ind"])

    Sh_ExposureRes=Sh_ExposureRes.join(nonstruct_Res, how='right', sort=True)
    Sh_ExposureCom=Sh_ExposureCom.join(nonstruct_Com, how='right', sort=True)
    Sh_ExposureInd=Sh_ExposureInd.join(nonstruct_Ind, how='right', sort=True)

    contents_Res=pd.DataFrame(np.array(contents_Res),columns=["contents_Res"])
    contents_Com=pd.DataFrame(np.array(contents_Com),columns=["contents_Com"])
    contents_Ind=pd.DataFrame(np.array(contents_Ind),columns=["contents_Ind"])

    Sh_ExposureRes=Sh_ExposureRes.join(contents_Res, how='right', sort=True)
    Sh_ExposureCom=Sh_ExposureCom.join(contents_Com, how='right', sort=True)
    Sh_ExposureInd=Sh_ExposureInd.join(contents_Ind, how='right', sort=True)

    print("--- %s seconds ---" % (time.time() - start_time))
