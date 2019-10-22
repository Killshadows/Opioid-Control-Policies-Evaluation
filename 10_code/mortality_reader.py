
# mortality_reader.py
# Author: Shota Takeshima
# Oct 20, 2019
# importing necessary libraries.

import pandas as pd
import numpy as np
import os

# path of the directory that includes mortality data files.
dirPath = '../00_source/'
# format of the mortality data file
fileNameFormat = "Underlying Cause of Death, %d.txt"

# output file path
outputPath = "../20_intermediate_files/pairB_intermidiate.csv"

# extracting condition for state.
# cond_states = ['FL', 'TX', 'WA']
# extracting condition for the cause of death
# extract rows that includes the cause like cond_cause.
cond_cause = "Drug poisonings"

# create  am empty data frame as a result data frame.
result = None

# Using for loop, first extract year, state, county and Deaths_county that match our conditions.
for i in range(2004, 2015 + 1):
    path = dirPath + fileNameFormat % i
    tmp = pd.read_csv(path, delimiter='\t')
    
    # remove 'the Notes' column, then drop NaN values.
    tmp = tmp.drop('Notes', axis = 1).dropna()
    
    # 'County' column in Raw data includes both county name and state name.
    # So, using split function, divide it to two columns.
    tmp_county = tmp.County.apply(lambda c: str(c).split(',')[0])
    tmp_state = tmp.County.apply(lambda c: str(c).split(',')[1].strip())
    
    tmp['County'] = tmp_county
    tmp['State'] = tmp_state

    # Extract necessary rows using conditions
    tmp_extracted = tmp[(tmp['Drug/Alcohol Induced Cause'].str.contains(cond_cause))\
                        #& (tmp.State.isin(cond_states))\
    ]
    
    # Assign or append the extracted rows to result.
    if(result is None):
        result = tmp_extracted
    else:
        result = result.append(tmp_extracted)

result.to_csv(outputPath)
