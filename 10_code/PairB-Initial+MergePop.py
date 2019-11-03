######## README ########

# For easier bugs checking and fixing
# This .py text file only makes the first step to initiate basic datasets for mortality analysis
# Only includes basic subsetting and reshaping

# The code below mainly initiates 2 basic mortality dataframes on county and state level respectively
# The next step would be merge with population dataset to do normalization


import pandas as pd
import numpy as np

# Import data from source dataset
mortality_int = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-2/master/20_intermediate_files/pairB_intermidiate.csv?token=ALEXUKHAZ57FEC5LR4TH3VS5YWJHK')
mortality_int


######## Learn more about the Initial Dateset ########

# We want to check if there are counties that have same names.
# We found that the number of county code is greater than the number of county names
# So we should use 'State' AND 'County' together as an identifier
CountyName_number = len(mortality_int['County'].unique())
CountyCode_number = len(mortality_int['County Code'].unique())
print('Number of county names =', CountyName_number)
print('Number of county codes =', CountyCode_number)

# Note that there are 3 specific reasons for drug overdose
# But we don't want to analyze into that much details
# We just want sum them up and configure them all as general drug overdose
# By that we simply drop 'Drug/Alcohol Induced Cause' and 'Drug/Alcohol Induced Cause Code' coloumn
mortality_int['Drug/Alcohol Induced Cause'].value_counts()

# Therefore, to form our intermdiate dataset, we only need 4 variables in mortality_int
# They are 'Year','State','County' and 'Deaths'
mortality_all = mortality_int[['Year','State','County','Deaths']]
mortality_all

# Check the current type of 'Deaths',
# Look at all the values of age to figure out if there is missing data or categorial data
for i in mortality_all.Deaths.value_counts().index: print(i)

# replace Missing entries with '0'
mortality_all[mortality_all['Deaths'] == 'Missing'] = '0'

# convert 'Deaths' from a categorical to numeric (float)
mortality_all['Deaths'] = mortality_all['Deaths'].astype('float')

# convert Missing data from '0' to 'NA'
mortality_all[mortality_all['Deaths'] == 0.0] = np.nan

# Take a look after data cleaning
mortality_all


######## County Level Mortality Dataset ########

# Sum up deaths caused by all types of drug overdose at county level
mortality_county = mortality_all.groupby(['Year','State','County']).sum().reset_index()
mortality_county

# Check if our groupby is correct
# i.e. Check duplications based on multiple columns on 'Year', 'State' AND 'County'
assert not mortality_county.duplicated(['Year','State','County']).any()


######## State Level Mortality Dataset ########
# Sum up deaths caused by all types of drug overdose at state level
mortality_state = mortality_all.groupby(['Year','State']).sum().reset_index()
mortality_state

# Check if our groupby is correct
# i.e. Check duplications based on multiple columns on 'Year' AND 'State'
assert not mortality_state.duplicated(['Year','State']).any()


######## Country Level Mortality Dataset (only for reference) ########
# Sum up deaths caused by all types of drug overdose at Country(USA) level
# aka time trends in whole USA
mortality_USA = mortality_all.groupby('Year').sum().reset_index()
mortality_USA
