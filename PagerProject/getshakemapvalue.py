import numpy as np
from sklearn.discriminant_analysis import StandardScaler
from sklearn.neighbors import NearestNeighbors
import sklearn.preprocessing

def getshakemapvalue(shakeoutput, Exposure):
    expo_lat=np.array(Exposure["LATITUDE"])
    expo_lon=np.array(Exposure["LONGITUDE"])
    shake_coords = [[], []]
    shake_gm = [[], [], [], [], [], [], []]

    #Have to figure out how we can we get only the column data for the xml file. It seems challenging
    for i in range(0, len(shakeoutput.grid)):
        shake_coords[0].append(shakeoutput.grid[i]['LON'])
        shake_coords[1].append(shakeoutput.grid[i]['LAT'])
        shake_gm[0].append(shakeoutput.grid[i]['MMI'])
        shake_gm[1].append(shakeoutput.grid[i]['PGA'])
        shake_gm[2].append(shakeoutput.grid[i]['PGV'])
        shake_gm[3].append(shakeoutput.grid[i]['PSA03'])
        shake_gm[4].append(shakeoutput.grid[i]['PSA10'])
        shake_gm[5].append(shakeoutput.grid[i]['PSA30'])
        shake_gm[6].append(shakeoutput.grid[i]['SVEL'])
    
    max_lon=max(shake_coords[0])
    min_lon=min(shake_coords[0])

    max_lat=max(shake_coords[1])
    min_lat=min(shake_coords[1])

    ######### PROBLEM SECTION, MAY BE SKETCHY!!! USE WITH CAUTION #########
    idx = np.where( np.logical_and((expo_lon >= min_lon), (expo_lon <= max_lon)) & np.logical_and((expo_lat >= min_lat), (expo_lat <= max_lat)))[0]

    expo_coords = [expo_lon[idx], expo_lat[idx]]


    '''scaler= StandardScaler()
    shake_coords_standardized= scaler.fit_transform(shake_coords)
    expo_coords_standardized= scaler.fit_transform(expo_coords)


    knn = NearestNeighbors(n_neighbors=2)
    knn.fit(shake_coords_standardized)
    dis, indices = knn.kneighbors(expo_coords_standardized)
    print(indices)
'''
    
