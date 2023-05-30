import numpy as np
from ismember import ismember


def calcfunstructfrag(sm_expo, structfrag, taxonomymap,countrystructfrag):
    unique_sm_tax =set(sm_expo['TAXONOMY'])
    #print(unique_sm_tax)

    damage_states =set(structfrag['Damage_state'])

    
    tax_idx = np.array(taxonomymap.loc[taxonomymap['taxonomy'].isin(unique_sm_tax)].index)

    for current_damage_states in damage_states:
        structfrag_sub=structfrag[structfrag['Damage_state']==current_damage_states] #structfrag_sub = structfrag(structfrag.Damage_state==damage_states(j),:); This is done


        print(len(structfrag_sub['Building_class']))
        vuln_idx = np.array(structfrag_sub.loc[~structfrag_sub['Building_class'].isin(taxonomymap['conversion'][tax_idx])].index)
        print(vuln_idx)
        print(len(vuln_idx))
    
    
    
    
    
    
    
    
    #return result, damage_states
    
    return 0, 0
