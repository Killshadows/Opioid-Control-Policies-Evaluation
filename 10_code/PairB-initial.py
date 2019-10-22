######## README ########

# For the sake of easier bugs checking and fixing, This .py text file is only the first step to initiate basic datasets for mortality analysis, which only includes basic subsetting and reshaping.
# The code below mainly initiates three basic mortality DataFrame on county, state and country level respectively.

# Code to form the intermediate dataset ready for use will be in another .py text file in the next step.
# Specifically, the next step would be examining statistic summary and selecting samples. After that, we can add the Post and Policy_State binary variables to these basic datasets in order to form our intermediate dataset.



import pandas as pd
import numpy as np

######## Import data from original dataset ########
# Note the URL need modification, as Shota will upload an updated version of raw data on GitHub later
mortality_int = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/estimating-impact-of-opioid-prescription-regulations-team-2/master/00_source/pairB_intermidiate.csv?token=ALEXUKH3VPP2OC65MMLV4Z25W4QSO')
mortality_int.head()


######## Learn more about the Initial Dateset ########

# We want to check if there are counties that have same names.
# The number of 'County Code' is greater than the number of 'County'.
# So we should use both 'State' AND 'County' to ensure a unique County.
County_number = len(mortality_int['County'].value_counts())
CountyCode_number = len(mortality_int['County Code'].value_counts())
County_number < CountyCode_number

# Note that there are 3 specific reasons for drug overdose
# But we don't want to analyze into that much details
# We just want sum them up and configure them all as general drug overdose
# By that we simply drop 'Drug/Alcohol Induced Cause' and 'Drug/Alcohol Induced Cause Code'
mortality_int['Drug/Alcohol Induced Cause'].value_counts()

# To form our intermdiate dataset, we only need 4 variables in mortality_int
# They are 'Year','State','County' and 'Deaths'
mortality_county = mortality_int[['Year','State','County','Deaths']]
mortality_county


######## County Level Mortality Dataset ########

# Sum up deaths caused by all types of drug overdose at county level, using groupby in pandas
# Also set dictionary to define a unique county in a specific year
dic_county_unique = ['Year','State','County']
mortality_by_county = mortality_county.groupby(dic_county_unique).sum().reset_index()
mortality_by_county

# List all counties in each state and count
county_list = mortality_by_county[['State','County']].groupby(['State','County']).count().reset_index()
print(county_list)
county_list['State'].value_counts()

# Check if our groupby is correct
# i.e. Check duplications based on multiple columns on 'Year', 'State' AND 'County'
assert not mortality_by_county.duplicated(['Year','State','County']).any()


######## State Level Mortality Dataset ########

mortality_state = mortality_int[['Year','State','Deaths']]

# Sum up deaths caused by all types of drug overdose at state level, using groupby in pandas
# Also set dictionary to define a unique state in a specific year
dic_state_unique = ['Year','State']
mortality_by_state = pd.DataFrame(mortality_state.groupby(dic_state_unique).sum().reset_index())
mortality_by_state

# List all states
mortality_by_state['State'].value_counts()

# Check if our groupby is correct
# i.e. Check duplications based on multiple columns on 'Year' AND 'State'
assert not mortality_by_state.duplicated(['Year','State']).any()


######## Country Level Mortality Dataset ########

mortality_USA = mortality_int[['Year','Deaths']]

# Sum up deaths caused by all types of drug overdose at Country(USA) level, using groupby in pandas
# Also set dictionary to define wholespecific year
mortality_all_USA = mortality_USA[['Year','Deaths']].groupby('Year').sum().reset_index()
mortality_all_USA


######## DataFrame Index ########
# County Level Mortality Dataset >>>
# mortality_by_county

# State Level Mortality Dataset >>>
# mortality_by_state

# Country Level Mortality Dataset >>>
# mortality_all_USA