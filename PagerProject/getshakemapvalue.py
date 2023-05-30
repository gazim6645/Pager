import numpy as np
import pandas as pd




from scipy.spatial import cKDTree

def pt_idx(shake_coords, expo_coords):
  """Gets the index of the nearest neighbor in shake_coords for each point in expo_coords.

  Args:
    shake_coords: An MX-by-2 matrix, where the first column
      contains the longitudes and the second column contains the latitudes
      of the shakeoutput points.
    expo_coords: An MY-by-2 matrix, where the first column
      contains the longitudes and the second column contains the latitudes
      of the exposure_res points.

  Returns:
    pt_idx: A column vector with MY rows. Each row in pt_idx contains the index of
      the nearest neighbor in shake_coords for the corresponding row in expo_coords.
  """

  # Create the KDTree object.
  kdtree = cKDTree(shake_coords)

  # Find the nearest neighbor in shake_coords for each point in expo_coords.
  pt_idx = kdtree.query(expo_coords, k=1)[1]

  return pt_idx




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

    shake_coords=np.array([(a,b) for a,b in zip(*shake_coords)])
    expo_coords=np.array([(a,b) for a,b in zip(*expo_coords)])


    pt = pt_idx(np.array(shake_coords), np.array(expo_coords))

    shake_gm=np.array(shake_gm)
    shake_gm = np.transpose(shake_gm)

    gmvalues = pd.DataFrame(shake_gm, columns=['MMI', 'PGA', 'PGV', 'PSA03', 'PSA10', 'PSA30', 'SVEL'])

    
    gmvalues = gmvalues.loc[pt]
    Exposure=Exposure.loc[idx]

    gmvalues=gmvalues.reset_index()
    del gmvalues['index']

    Exposure=Exposure.reset_index()
    del Exposure['index']


    ShakeMap_Exposure = Exposure.join(gmvalues, how='right', sort=True)
   # ShakeMap_Exposure = ShakeMap_Exposure.reset_index()
    #del ShakeMap_Exposure['index']
    #ShekeMap_Exposure =Exposure.join(gmvalues, how='')
    print(ShakeMap_Exposure.iloc[685120]['SVEL'])
    print(ShakeMap_Exposure.head)
    



    
