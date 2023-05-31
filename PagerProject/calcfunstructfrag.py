import numpy as np
import pandas as pd


def calcfunstructfrag(sm_expo, structfrag, taxonomymap,countrystructfrag):
    unique_sm_tax =set(sm_expo['TAXONOMY'])
    
    damage_states =set(structfrag['Damage_state'])

    
    tax_idx = set(np.array(taxonomymap.loc[taxonomymap['taxonomy'].isin(unique_sm_tax)].index))
    
    
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
        vuln_idx = []
        for i in taxonomymap['conversion'][tax_idx]:
            curr_idx = structfrag_sub.loc[structfrag_sub['Building_class'] == i].index
            vuln_idx.append(curr_idx[0])
        

        '''
        a=find(tax_idx==0);
        b=find(vuln_idx==0);
        if length(a)>=1 || length(b)>=1
            
        pause;
        end
        '''
        df1 = pd.DataFrame(structfrag_sub.iloc[vuln_idx]).reset_index()
        del df1['index']
        df2 = pd.DataFrame(taxonomymap['taxonomy'][tax_idx]).reset_index()
        del df2['index']
        vuln_table = df2.join(df1, how='right', sort=True)
        print(vuln_table)

    '''
    if istable(countrystructfrag)
        countrystructfrag_sub=countrystructfrag(countrystructfrag.Damage_state(j),:);
        [~,iglobal,icountry] = intersect(vuln_table.Building_class,countrystructfrag_sub.Building_class);
        vuln_table(iglobal,:) = [vuln_table(iglobal,"taxonomy") countrystructfrag_sub(icountry,:)];
    end
    '''
    
    
    
    
    #return result, damage_states
    
    return 0, 0
