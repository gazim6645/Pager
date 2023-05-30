import numpy as np
from ismember import ismember


def calcfunstructfrag(sm_expo, structfrag, taxonomymap,countrystructfrag):
    unique_sm_tax =set(sm_expo['TAXONOMY'])
    #print(unique_sm_tax)

    damage_states =set(structfrag['Damage_state'])

    
    tax_idx = np.array(taxonomymap.loc[taxonomymap['taxonomy'].isin(unique_sm_tax)].index)

    for current_damage_states in damage_states:
        structfrag_sub=structfrag[structfrag['Damage_state']==current_damage_states] #structfrag_sub = structfrag(structfrag.Damage_state==damage_states(j),:); This is done

        structfrag_sub=structfrag_sub.reset_index()
        del structfrag_sub['index']

        
        
        varOne=structfrag_sub['Building_class']
        varTwo=taxonomymap['conversion'][tax_idx]


        #vuln_idx = np.array(varTwo.isin(varOne))
        vuln_idx=np.isin(varTwo, varOne)
        print(len((vuln_idx)))
        print(vuln_idx)
        break

        
    
    
    
    
    
    
    
    
    #return result, damage_states
    
    return 0, 0
