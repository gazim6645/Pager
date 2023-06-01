from cmath import isnan
from re import X
import numpy as np
import pandas as pd
from itertools import zip_longest


def calcfunstructfrag(sm_expo, structfrag, taxonomymap,countrystructfrag):
    unique_sm_tax =set(sm_expo['TAXONOMY'])
    
    damage_states =set(structfrag['Damage_state'])

    
    
    tax_idx = np.array(taxonomymap.loc[taxonomymap['taxonomy'].isin(unique_sm_tax)].index)
    
    
    for current_damage_states in damage_states:
        current_damage_states="slight"
        
        structfrag_sub=structfrag[structfrag['Damage_state']==current_damage_states] #structfrag_sub = structfrag(structfrag.Damage_state==damage_states(j),:); This is done

        structfrag_sub=structfrag_sub.reset_index()
        del structfrag_sub['index']

        
       

        #vuln_idx=np.array(structfrag_sub.loc[taxonomymap['conversion'][tax_idx].isin(structfrag_sub['Building_class'])])
        #vuln_idx=structfrag_sub.loc[structfrag_sub['Building_class'].isin(taxonomymap['conversion'][tax_idx])].index
        #, drop_duplicates=False)
        #vuln_idx=structfrag_sub.loc[structfrag_sub['Building_class'].isin(taxonomymap['conversion'][tax_idx]), keep_duplicates=False].index
        #vuln_idx=structfrag_sub[structfrag_sub['Building_class'].isin(taxonomymap['conversion'][tax_idx])]
        #print(len(taxonomymap['conversion'][tax_idx]))
        #print(len(taxonomymap['conversion'][tax_idx].unique()))
        
        

        # from matlab code seems unnecessary
        '''
        a=find(tax_idx==0);
        b=find(vuln_idx==0);
        if length(a)>=1 || length(b)>=1
            
        pause;
        end
        '''

        
        # previous way of combining tables, works but new way doesn't use for loop
        
        vuln_idx = []

        for i in taxonomymap['conversion'][tax_idx]:
            curr_idx = structfrag_sub.loc[structfrag_sub['Building_class'] == i].index
            vuln_idx.append(curr_idx[0])
        df1 = pd.DataFrame(structfrag_sub.iloc[vuln_idx]).reset_index()
        del df1['index']
        df2 = pd.DataFrame(taxonomymap['taxonomy'][tax_idx]).reset_index()
        del df2['index']
        vuln_table = df2.join(df1, how='right', sort=True)

        
        '''
        # improved way of combining taxonomy map with structfrag_sub
        df1 = pd.DataFrame(taxonomymap['conversion'][tax_idx]).reset_index() 
        del df1['index']

        structfrag_sub = structfrag_sub.rename(columns={'Building_class': 'conversion'})
        vuln_table = pd.merge(df1, structfrag_sub, how='inner', on=['conversion'])

        df2 = pd.DataFrame(taxonomymap['taxonomy'][tax_idx]).reset_index()
        del df2['index']
        
        vuln_table = df2.join(vuln_table, how='right', sort=True)
        vuln_table = vuln_table.rename(columns={'conversion': 'Building_class', 'taxonomy': 'TAXONOMY'})
        structfrag_sub = structfrag_sub.rename(columns={'conversion': 'Building_class'})
        '''

        # again, seems unnecessary
        '''
        if istable(countrystructfrag)
            countrystructfrag_sub=countrystructfrag(countrystructfrag.Damage_state(j),:);
            [~,iglobal,icountry] = intersect(vuln_table.Building_class,countrystructfrag_sub.Building_class);
            vuln_table(iglobal,:) = [vuln_table(iglobal,"taxonomy") countrystructfrag_sub(icountry,:)];
        end
        '''
    
        vuln_table = vuln_table.rename(columns={'taxonomy': 'TAXONOMY'})
        sm_vuln_table = pd.merge(sm_expo['TAXONOMY'], vuln_table, how='inner', on=['TAXONOMY'])


        #need to fix sm_vuln_table
        
        shake_input = [0]*len(sm_vuln_table)
        """
        val_pga = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="PGA"].index)
        val_sa3 = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="SA(0.3s)"].index)
        val_sa1 = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="SA(1.0s)"].index)
      
        pga=dict(zip_longest(val_pga, np.array(sm_expo['PGA'][val_pga]), fillvalue=None))
        
        sa3=dict(zip_longest(val_sa3, np.array(sm_expo['PSA03'][val_sa3]), fillvalue=None))
        
        sa1=dict(zip_longest(val_sa1, np.array(sm_expo['PSA10'][val_sa1]), fillvalue=None))"""
        val_pga = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="PGA"].index)
        val_sa3 = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="SA(0.3s)"].index)
        val_sa1 = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="SA(1.0s)"].index)
      
        shake_dict = dict(zip_longest(val_pga, np.array(sm_expo['PGA'][val_pga]), fillvalue=None))
        
        shake_dict.update(dict(zip_longest(val_sa3, np.array(sm_expo['PSA03'][val_sa3]), fillvalue=None)))
        
        shake_dict.update((zip_longest(val_sa1, np.array(sm_expo['PSA10'][val_sa1]), fillvalue=None)))
        

        shake_input = np.array(list(shake_dict.values()))
        shake_input = shake_input/100
        
        #sm_expo["COST_STRUCTURAL_USD"][400]=np.nan

        #we have to make test cases where this fails
        sk=sm_expo.loc[sm_expo["COST_STRUCTURAL_USD"].isna()].index
        
        

        if(len(sk)!=0):
            
            sm_expo["COST_STRUCTURAL_USD"][sk]=0.7*sm_expo["TOTAL_REPL_COST_USD"][sk]

        tabV=(sm_vuln_table.iloc[:,4:]).to_numpy()
        print(tabV)

        



        break



        
    
    
    
    
    #return result, damage_states
    
    return 0, 0
