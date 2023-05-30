import numpy as np
from ismember import ismember


def calcfunstructfrag(sm_expo, structfrag, taxonomymap,countrystructfrag):
    unique_sm_tax =sm_expo['TAXONOMY']
    #print(unique_sm_tax)

    damage_states =set(structfrag['Damage_state'])

    
    tax_idx = np.array(taxonomymap.loc[taxonomymap['taxonomy'].isin(unique_sm_tax)].index)
    
    for current_damage_states in damage_states:
        
        structfrag_sub=structfrag[structfrag['Damage_state']==current_damage_states] #structfrag_sub = structfrag(structfrag.Damage_state==damage_states(j),:); This is done

        structfrag_sub=structfrag_sub.reset_index()
        del structfrag_sub['index']

        vuln_idx=np.array(structfrag_sub.loc[structfrag_sub['Building_class'].isin(taxonomymap['conversion'][tax_idx])].index)
        
        '''
        a=find(tax_idx==0);
        b=find(vuln_idx==0);
        if length(a)>=1 || length(b)>=1
            
        pause;
        end
        '''

        print(taxonomymap['taxonomy'][tax_idx])
        print(structfrag_sub.iloc[vuln_idx])
        vuln_table = taxonomymap['taxonomy'][tax_idx].join(structfrag_sub.iloc[vuln_idx], how='right', sort=True);
        print(vuln_table)
    
    
        break
    
    
    
    
    
    #return result, damage_states
    
    return 0, 0
