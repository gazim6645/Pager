
from itertools import zip_longest
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


imls = [0.05,0.0562,0.0631,	0.0709,	0.0796,	0.0895,	0.1005,	0.1129,	0.1269,	0.1425,	0.1601,	0.1799	,0.2021,0.2271,0.2551,0.2866,0.322,0.3617,0.4064,0.4565,0.5129,	0.5762,	0.6474,	0.7273,	0.8171,	0.9179,	1.0312,	1.1585	,1.3016	,1.4622	,1.6428	,1.8456,2.0734,	2.3294,	2.6169,	2.94,3.3029,3.7106,	4.1687,	4.6833,	5.2615,	5.911,6.6407,7.4605,8.3815,9.4162,10.5787,11.8846,13.3517,15]

def calcfunnonstrutcexp(sm_expo, nonstructvuln, taxonomymap,countrynonstructvuln):

    unique_sm_tax =set(sm_expo['TAXONOMY'])

    result= []
    
    tax_idx = np.array(taxonomymap.loc[taxonomymap['taxonomy'].isin(unique_sm_tax)].index)


    vuln_idx = []

    for i in taxonomymap['conversion'][tax_idx]:
        curr_idx = nonstructvuln.loc[nonstructvuln['Building_class'] == i].index
        vuln_idx.append(curr_idx[0])
    df1 = pd.DataFrame(nonstructvuln.iloc[vuln_idx]).reset_index()
    del df1['index']
    df2 = pd.DataFrame(taxonomymap['taxonomy'][tax_idx]).reset_index()
    del df2['index']
    vuln_table = df2.join(df1, how='right', sort=True)


    vuln_table = vuln_table.rename(columns={'taxonomy': 'TAXONOMY'})
    sm_vuln_table = pd.merge(sm_expo['TAXONOMY'], vuln_table, how='inner', on=['TAXONOMY'])

    shake_input = [0]*len(sm_vuln_table)

    val_pga = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="PGA"].index)
    val_sa3 = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="SA(0.3s)"].index)
    val_sa1 = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="SA(1.0s)"].index)
      
    shake_dict = dict(zip_longest(val_pga, np.array(sm_expo['PGA'][val_pga]), fillvalue=None))
        
    shake_dict.update(dict(zip_longest(val_sa3, np.array(sm_expo['PSA03'][val_sa3]), fillvalue=None)))
        
    shake_dict.update((zip_longest(val_sa1, np.array(sm_expo['PSA10'][val_sa1]), fillvalue=None)))
        
    shake_dict = dict(sorted(shake_dict.items())) 
    shake_input = np.array(list(shake_dict.values()))

    shake_input = shake_input/100


    #sm_expo["COST_STRUCTURAL_USD"][400]=np.nan
        #we have to make test cases where this fails
    sk=sm_expo.loc[sm_expo["COST_NONSTRUCTURAL_USD"].isna()].index
        
    if(len(sk)!=0):
            
        sm_expo["COST_NONSTRUCTURAL_USD"][sk]=0.7*sm_expo["TOTAL_REPL_COST_USD"][sk]

    tabV=(sm_vuln_table.iloc[:,3:]).to_numpy()
    SI=shake_input

    #cost_ratio=np.array([np.interp(SI[i], imls, tabV[i], left=0) for i in range(SI.size)]) 
    '''
    cost_ratio = []
    for i in range(SI.size):
        f=interp1d(imls, tabV[i],  fill_value='extrapolate') 
        curr = f(SI[i]).max()
        if (curr < 0):
            curr = 0
        cost_ratio.append(curr)
    '''
    cost_ratio=[]
    for i in range(SI.size):
        if(SI[i] <imls[0]):
            cost_ratio.append((interp1d(imls, tabV[i],  fill_value='extrapolate'))(SI[i]))
        else:
            cost_ratio.append(np.interp(SI[i], imls, tabV[i]))

    
    cost_ratio = np.array(cost_ratio)
    cost_ratio[cost_ratio < 0] = 0
    result=cost_ratio*sm_expo["COST_NONSTRUCTURAL_USD"]
    return result


    
