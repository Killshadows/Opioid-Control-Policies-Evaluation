######## README ########
# Author: Jingyi Wu

# For easier bugs checking and fixing
# This .py text file only makes the first step to initiate basic datasets for mortality analysis
# Only includes basic subsetting and reshaping

# The code below mainly initiates two basic mortality dataframes on county and state level respectively
# Specifically, the Initial Dataset is the dataframe - 'mortality'
# The next step would be merge with population dataset to do normalization


import pandas as pd
import numpy as np

# Import data from source dataset
mortality_int = pd.read_csv('~/estimating-impact-of-opioid-prescription-regulations-team-2/20_intermediate_files/pairB_intermidiate.csv')
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

# Check if there is missed information
# Seems no missing information in WA, FL and TX
# But do have missing in some other states
miss = merge_mortality[merge_mortality['_merge'] != 'both']
miss
miss['_merge'].value_counts()
miss[(miss['State_Code'] == 'WA')|(miss['State_Code'] == 'FL')|(miss['State_Code'] == 'TX')]

# Check which state has missing information
miss['State_Name'].value_counts()

# Check if there is different naming for DC
import re
for i in state_dic['State_Name'].unique():
    if re.match(".*D.*",i):
        print(i)

# Go back to original dictionary data to verify
state_dic[(state_dic['State_Name']=='District of Columbia')|(state_dic['State_Name']=='D.C.')]

# Unify the naming for District of Columbia
state_dic['State_Name'][state_dic['State_Name'] == 'D.C.'] = 'District of Columbia'

# Check if there is different naming for Rhode Island and Providence Plantations
for i in state_dic['State_Name'].unique():
    if re.match(".*hode.*",i):
        print(i)      
        
# Go back to original dictionary data to verify
state_dic[(state_dic['State_Name']=='Rhode Island')|(state_dic['State_Name']=='Rhode Island and Providence Plantations')]

# Unify the naming for Rhode Island and Providence Plantations
state_dic['State_Name'][state_dic['State_Name'] == 'Rhode Island and Providence Plantations'] = 'Rhode Island'

# Check if there is different naming for New Mexico, Indiana and Pennsylvania
# seems they are not from the problem of different naming
for i in state_dic['State_Name'].unique():
    if re.match(".*exi.*",i):
        print(i)
for i in state_dic['State_Name'].unique():
    if re.match(".*ndia.*",i):
        print(i)
for i in state_dic['State_Name'].unique():
    if re.match(".*enns.*",i):
        print(i)        


# Redo merge first
merge_dic = pd.merge(mortality, state_dic, how='left', on='State_Code')
merge_dic = merge_dic[['Year', 'State_Code', 'State_Name', 'County', 'Deaths']]
merge_mortality = pd.merge(merge_dic, pop, how='left', on=['State_Name','County'], indicator=True)

# Check still missing information
merge_mortality['_merge'].value_counts()
miss = merge_mortality[merge_mortality['_merge'] != 'both']
miss

# Check if there is something wrong with Mc Kean County in pop data
for i in pop['County'].unique():
    if re.match(".*ean.*",i):
        print(i)
for i in mortality['County'].unique():
    if re.match(".*ean.*",i):
        print(i)
# Unify the naming for Mc Kean County
pop['County'][pop['County']=='McKean County'] = 'Mc Kean County'

# Check if there is something wrong with Dona Ana County in pop data
for i in pop['County'].unique():
    if re.match(".*Ana.*",i):
        print(i)
for i in mortality['County'].unique():
    if re.match(".*Ana.*",i):
        print(i)
# Unify the naming for Dona Ana County
pop['County'][pop['County']=='Doña Ana County'] = 'Dona Ana County'

# Check if there is something wrong with La Porte County in pop data
for i in pop['County'].unique():
    if re.match(".*orte.*",i):
        print(i)
for i in mortality['County'].unique():
    if re.match(".*orte.*",i):
        print(i)  
# Unify the naming for La Porte County
pop['County'][pop['County']=='LaPorte County'] = 'La Porte County'

# Redo merge again
merge_dic = pd.merge(mortality, state_dic, how='left', on='State_Code')
merge_dic = merge_dic[['Year', 'State_Code', 'State_Name', 'County', 'Deaths']]
merge_mortality = pd.merge(merge_dic, pop, how='left', on=['State_Name','County'], indicator=True)

# Check still missing information
# Ignore Alaska and will drop it later
merge_mortality['_merge'].value_counts()
miss = merge_mortality[merge_mortality['_merge'] != 'both']
miss

# Reset index of merged data
merge_mortality = merge_mortality.reset_index(drop=True)

# Check if there is NaN in population for WA, FL and TX
# We got our merged dataset ready for the next step
assert not merge_mortality[(merge_mortality['State_Code']=='WA')|(merge_mortality['State_Code']=='FL')|(merge_mortality['State_Code']=='TX')]['Population_2010'].isnull().any()

# Normalization by 2010 Population
merge_mortality['Deaths_NormPop2010'] = merge_mortality['Deaths']/ merge_mortality['Population_2010']
merge_mortality.head()

# Extract necessary columns for next step
# Rename the columns the same as required in action plan
mortality_pop_norm = merge_mortality[['Year','State_Code','County','Deaths','Population_2010','Deaths_NormPop2010']]
mortality_pop_norm.columns = ['Year','State','County','Deaths','Population','Deaths_PerCap_County']
mortality_pop_norm
