from filecmp import cmp
from lib2to3.pgen2.pgen import DFAState
import pandas as pd

def read_files(ind_ccode):#This will retun the country and the files associated with it
    ccode_files=[]
    country_name, region_name= find_file_end(ind_ccode)
    if (country_name == "no_match"):
        print('WARNING: no matching exposure files for country code')
    else: 
        ccode_files.append("Exposure_Res_%s.csv" %country_name)
        ccode_files.append('Exposure_Com_%s.csv' %country_name)
        ccode_files.append('Exposure_Ind_%s.csv' % country_name)
        ccode_files.append('struct_vulnerability_%s.csv' %country_name)        
        ccode_files.append('struct_vulnerability_%s.csv' %region_name)        
        ccode_files.append('nonstruct_vulnerability_%s.csv' % country_name)        
        ccode_files.append('nonstruct_vulnerability_%s.csv' % region_name)        
        ccode_files.append('contents_vulnerability_%s.csv' %country_name)        
        ccode_files.append('contents_vulnerability_%s.csv' % region_name)        
        ccode_files.append('taxonomy_mapping_%s.csv' % country_name)        
        ccode_files.append('taxonomy_mapping_%s.csv'% region_name)

    return ccode_files, country_name








def find_file_end(ind_ccode): #This will return the country name and the region name
    countries = pd.read_csv("countries.csv")

    row = countries[countries['ccode'] == ind_ccode]

    country_name = row['country_name'].values[0]
    region_name = row['region_name'].values[0]
    
    return str(country_name), str(region_name)