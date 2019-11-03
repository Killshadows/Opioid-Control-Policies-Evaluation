######## README ########

# For easier bugs checking and fixing
# This .py text file only makes the first step to initiate basic datasets for mortality analysis
# Only includes basic subsetting and reshaping

# The code below mainly initiates two basic mortality dataframes on county and state level respectively
# Specifically, the Initial Dataset is the dataframe - 'mortality'
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
mortality = mortality_all.groupby(['Year','State','County']).sum().reset_index()
mortality.columns = ['Year', 'State_Code', 'County', 'Deaths']
mortality

# Check if our groupby is correct
# i.e. Check duplications based on multiple columns on 'Year', 'State' AND 'County'
assert not mortality.duplicated(['Year','State_Code','County']).any()


######## State Level Mortality Dataset ########
# Sum up deaths caused by all types of drug overdose at state level
# mortality_state = mortality.groupby(['Year','State']).sum().reset_index()
# mortality_state

# Check if our groupby is correct
# i.e. Check duplications based on multiple columns on 'Year' AND 'State'
# assert not mortality_state.duplicated(['Year','State']).any()



######## README ########

# Mainly contains population data cleaning and merging with Initial Dataset
# Specifically, the Merged Dataset is the dataframe - 'merge_mortality'
# The next step would be examining statistics and sample selection

# Import source data of population
pop = pd.read_excel('~/estimating-impact-of-opioid-prescription-regulations-team-2/00_source/Population2010_AllCounties.xls')
pop.head(10)
pop.tail(10)

# Subsetting to get necessary information
pop = pop.iloc[6:3229,0:4].copy().reset_index(drop=True)

# Rename columns for later merging check
pop.columns = ['County', 'State_Name', 'Population_2000', 'Population_2010']
pop = pop.dropna(how='all')
pop.tail()

# Check the dataframe after deleting NaN values
assert not pop['County'].isnull().any()

# Since we only have state name in population data
# and only state code in the initial dataset
# find a dictionary as mapping

# Import states name dictionary data
state_dic = pd.read_csv('~/estimating-impact-of-opioid-prescription-regulations-team-2/00_source/states_name_dic.csv')
# Rename columns for later merging check
state_dic.columns = ['State_Name','State_Code', 'FIPS']
state_dic.head()

# Merging county_level mortality data with dictionary data
merge_dic = pd.merge(mortality, state_dic, how='left', on='State_Code', indicator=True)

# Check if our merge is correct
both_check = merge_dic['_merge']=='both'
assert both_check.all()

# Extract necessary columns
# Could delete one state code column since '_merge' are all 'both'
merge_dic = merge_dic[['Year', 'State_Code', 'State_Name', 'County', 'Deaths']]
merge_dic.tail()

# Then merge with population data
merge_mortality = pd.merge(merge_dic, pop, how='left', on=['State_Name','County'], indicator=True)
merge_mortality.head()

# Check unmatched information in merging
merge_mortality['_merge'].value_counts()

# Check if there is missed information in DC, FL and TX
miss = merge_mortality[merge_mortality['_merge'] != 'both']
miss[(miss['State_Code'] == 'DC')|(miss['State_Code'] == 'FL')|(miss['State_Code'] == 'TX')]

# Check if there is different naming for a state
import re
for i in state_dic['State_Name'].unique():
    if re.match(".*D.*",i):
        print(i)

# Go back to original dictionary data to verify
state_dic[(state_dic['State_Name']=='District of Columbia')|(state_dic['State_Name']=='D.C.')]

# Unify the naming for District of Columbia
state_dic['State_Name'][state_dic['State_Name'] == 'D.C.'] = 'District of Columbia'

# Redo merge
merge_dic = pd.merge(mortality, state_dic, how='left', on='State_Code')
merge_dic = merge_dic[['Year', 'State_Code', 'State_Name', 'County', 'Deaths']]
merge_mortality = pd.merge(merge_dic, pop, how='left', on=['State_Name','County'], indicator=True)

# Check unmatched information
merge_mortality['_merge'].value_counts()

# There are still some unmatched
# Deal with them later if needed when come to sample selection
miss = merge_mortality[merge_mortality['_merge'] != 'both']
miss['State_Name'].value_counts()

# Drop state AK
merge_mortality = merge_mortality[merge_mortality['State_Code']!='AK'].reset_index(drop=True)

# Check if there is NaN in population for DC, FL and TX
# We got our merged dataset ready for the next step
assert not merge_mortality[(merge_mortality['State_Code']=='DC')|(merge_mortality['State_Code']=='FL')|(merge_mortality['State_Code']=='TX')]['Population_2010'].isnull().any()
