
def calcfunstructfrag(sm_expo, structfrag, taxonomymap,countrystructfrag):
    unique_sm_tax = set(sm_expo['TAXONOMY'])
    #print(unique_sm_tax)

    damage_states = set(structfrag['Damage_state'])
    
    for current_damage_states in damage_states:
        structfrag_sub=structfrag[structfrag['Damage_state']==current_damage_states] #structfrag_sub = structfrag(structfrag.Damage_state==damage_states(j),:); This is done
        print(structfrag_sub)
        



    #return result, damage_states
    
    return 0, 0