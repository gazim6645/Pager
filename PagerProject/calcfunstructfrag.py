import numpy as np
import pandas as pd
from itertools import zip_longest


def calcfunstructfrag(sm_expo, structfrag, taxonomymap,countrystructfrag):
    unique_sm_tax =set(sm_expo['TAXONOMY'])
    
    damage_states =set(structfrag['Damage_state'])

    
    
    tax_idx = np.array(taxonomymap.loc[taxonomymap['taxonomy'].isin(unique_sm_tax)].index)
    
    
    for current_damage_states in damage_states:
        
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
        '''
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

        # again, seems unnecessary
        '''
        if istable(countrystructfrag)
            countrystructfrag_sub=countrystructfrag(countrystructfrag.Damage_state(j),:);
            [~,iglobal,icountry] = intersect(vuln_table.Building_class,countrystructfrag_sub.Building_class);
            vuln_table(iglobal,:) = [vuln_table(iglobal,"taxonomy") countrystructfrag_sub(icountry,:)];
        end
        '''

        sm_expo_new = pd.DataFrame(sm_expo['TAXONOMY'])

        sm_vuln_table = pd.merge(sm_expo_new, vuln_table, how='inner', on=['TAXONOMY'])

        
        #shake_input = [0]*len(sm_vuln_table)
        val = np.array(sm_vuln_table.loc[sm_vuln_table["IMT"]=="PGA"].index)
        print(val)
        #shake_input[val] = np.array(sm_expo['PGA'][val])
        shake_input=dict(zip_longest(val, np.array(sm_expo['PGA'][val]), fillvalue=None))
        
        print(shake_input)

        break


        
    
    
    
    
    #return result, damage_states
    
    return 0, 0
