
#################### README ###################################
# This code include:
# 1. Some functions used frequently
# 2. Code for three states: FL, AL, GA
#    1) Read data（both Shipment data and Population data）
#    2）Transfer TRANSACTION_DATE to 'year & month'
#    3) Merge Shipment data with Poplulation data
#    4) Group by 'BUYER_STATE','BUYER_COUNTY', 'YEAR'
#    5) Normalize Shipment Quantity by Population
#    6) Pre-post plot
# 3. Diff-in-diff plot with three states

# Note: For diff-in-diff analysis, we pick the states most proximate to FL geographically: Alabama and Georgia


# import packages
import pandas as pd
import numpy as np
from plotnine import *



######### Some useful functions here ##########
'''
Read data
'''
def readData(path):
    df = pd.read_csv(path,
                     sep='\t',
                     usecols=['TRANSACTION_DATE', 'BUYER_STATE', 'BUYER_COUNTY', 'QUANTITY', 'BUYER_ZIP'])
    return df

'''
Transfer TRANSACTION_DATE to year & month
'''
def transferDate(df_shipments):
# Convert RTANSACTION_DATE to string in order to subset it
    df_shipments['TRANSACTION_DATE'] = df_shipments['TRANSACTION_DATE'].astype(str)
# Subset the TRANSACTION_DATE, and get YEAR and Month
    df_shipments['YEAR'] = df_shipments['TRANSACTION_DATE'].apply(lambda x: x[-4:])
    df_shipments['MONTH'] = df_shipments['TRANSACTION_DATE'].apply(lambda x: x[-8:-6])
# Convert to int, in order to use PeriodIndex
# Create a new col as YYYY-MM
    df_shipments['YEAR'] = df_shipments['YEAR'].astype(int)
    df_shipments['MONTH'] = df_shipments['MONTH'].astype(int)
    df_shipments['TRANSACTION_TIME'] = pd.PeriodIndex(year=df_shipments["YEAR"], month=df_shipments["MONTH"], freq="m")
    return df_shipments

'''
group by 'BUYER_STATE','BUYER_COUNTY', 'YEAR'
'''
def groupBy(shipment_merged):
    shipment_grouped = shipment_merged.groupby(['BUYER_STATE','BUYER_COUNTY', 'YEAR']).agg({'QUANTITY': 'sum', 'POP':'max'})
    shipment_grouped = shipment_grouped.reset_index()
    shipment_grouped.head()
    return shipment_grouped

'''
Normalization for Quantity
'''
# Normalize the quantity
def normalize(shipment_grouped):
    shipment_grouped['QUANTITY_PERCAP'] = shipment_grouped['QUANTITY']/shipment_grouped['POP']
    shipment_grouped['POST'] = (shipment_grouped.YEAR > 2009)*1
    return shipment_grouped

'''
Plot pre-post
'''
def plot(shipment_grouped, state_name):
    prePost = (ggplot(shipment_grouped,aes(x = 'YEAR', y = 'QUANTITY_PERCAP', group = 'POST'))
               + geom_point(alpha = 0.5)
               + geom_smooth(method='lm', fill=None, colour="red")
               +theme_classic(base_family = "Helvetica")
               +labs(title= f"opioid shipments Pre-Post analysis for {state_name}",
                     x="Year",
                     y="Quantity Per Cap"))
    # Save
    prePost.save(f'/Users/ZifanPeng/Desktop/estimating-impact-of-opioid-prescription-regulations-team-2/30_results/{state_name}-PrePost.png')





####### Import poplulation data ########
# Import poplulation dataset for all states and counties
pop = pd.read_excel('/Users/ZifanPeng/Desktop/IDS-data/Population2010_AllCounties.xls')
pop = pop.iloc[6:3229,0:4].copy().reset_index(drop=True)
pop.columns = ['County', 'State', 'Population_2000', 'Population_2010']
pop = pop.drop('Population_2000', axis = 1)
# We find that 2 rows are null, drop them
pop = pop.dropna(how='all')
# Make the format of 'County' the same as that in shipment dataset
pop['County'] = pop['County'].str.upper()
pop['County'] = pop['County'].str.replace(' COUNTY', '')
pop = pop.rename(columns={'Population_2010':'POP'})





###### Florida ########
# Import shipment data for Florida
shipments_FL = readData('/Users/ZifanPeng/Desktop/IDS-data/arcos-fl-statewide-itemized.tsv')
# Deal with NaN values
shipments_FL['BUYER_COUNTY'] = shipments_FL['BUYER_COUNTY'].replace(np.nan, 'PINELLAS')
# Check if we have nan value
assert (shipments_FL.isnull().any().sum())==0

# Transfer time
shipments_FL = transferDate(shipments_FL)

# Subset population for FL
pop_FL = pop[pop.State == 'Florida'].reset_index().drop('index', axis = 1)
pop_FL['County'] = pop_FL['County'].replace({'ST. LUCIE': 'SAINT LUCIE',
                                                          'ST. JOHNS': 'SAINT JOHNS',
                                                          'DESOTO': 'DE SOTO'})

# Merge
shipment_FL_merged = pd.merge(shipments_FL, pop_FL, left_on='BUYER_COUNTY', right_on='County',
                   how='left' ,validate = 'm:1', indicator=True)
# Check if 'both' merged
assert (shipment_FL_merged['_merge']=='both').all()
# Drop uncorrelated cols
shipment_FL_merged = shipment_FL_merged.drop( ['County', 'State','_merge'], axis = 1)

# Group by
shipment_FL_grouped = groupBy(shipment_FL_merged)

# normalize
normalize(shipment_FL_grouped)

# Plot
plot(shipment_FL_grouped, 'FL')

# Summary plot for FL
plotSummary = (ggplot(shipment_FL_grouped, aes(x = 'YEAR', y = 'QUANTITY', color ='BUYER_COUNTY'))
 +geom_line()
  +labs(title = "Opioid Shipments Quantity Trend in Florida",
                 x = "Year",
                 y = "Quantity",
                 color = "County")
)
plotSummary.save(f'/Users/ZifanPeng/Desktop/estimating-impact-of-opioid-prescription-regulations-team-2/30_results/FL_summary.png')





###### Alabama ######

# Import shipment data for Alabama
shipments_AL = readData('/Users/ZifanPeng/Desktop/IDS-data/arcos-al-statewide-itemized.tsv')
# Check if we have nan value
assert (shipments_AL.isnull().any().sum())==0
# Transfer time
shipments_AL = transferDate(shipments_AL)

# Merge shipment data with pop data for AL
# Subset population for AL
pop_AL = pop[pop.State == 'Alabama'].reset_index().drop('index', axis = 1)
# Fix the county name
pop_AL['County'] = pop_AL['County'].replace({'DEKALB': 'DE KALB',
                                                          'ST. CLAIR': 'SAINT CLAIR'})
# Merge
shipment_AL_merged = pd.merge(shipments_AL, pop_AL, left_on='BUYER_COUNTY', right_on='County',
                   how='outer' ,validate = 'm:1', indicator=True)
# Check if 'both' merged
assert (shipment_AL_merged['_merge']=='both').all()
# Drop uncorrelated cols
shipment_AL_merged = shipment_AL_merged.drop( ['County', 'State','_merge'], axis = 1)

# Group by
shipment_AL_grouped = groupBy(shipment_AL_merged)

# normalize
normalize(shipment_AL_grouped)

# Plot
plot(shipment_AL_grouped, 'AL')






####### Georgia ###########

# Import shipment data for Georgia
shipments_GA = readData('/Users/ZifanPeng/Desktop/IDS-data/arcos-ga-statewide-itemized.tsv')

# Deal with NaN values
shipments_GA['BUYER_COUNTY'].loc[shipments_GA['BUYER_ZIP']==31728]  = 'GRADY'
shipments_GA =shipments_GA[shipments_GA['BUYER_ZIP']!=30883]
# Check if we have nan value
assert (shipments_GA.isnull().any().sum())==0

# Transfer time
shipments_GA = transferDate(shipments_GA)

# Merge shipment data with pop data for GA
# Subset population for GA
pop_GA = pop[pop.State == 'Georgia'].reset_index().drop('index', axis = 1)
# Merge
shipment_GA_merged = pd.merge(shipments_GA, pop_GA, left_on='BUYER_COUNTY', right_on='County',
                   how='left' ,validate = 'm:1', indicator=True)
# Check if 'both' merged
assert (shipment_GA_merged['_merge']=='both').all()
# Drop uncorrelated cols
shipment_GA_merged = shipment_GA_merged.drop( ['County', 'State','_merge'], axis = 1)

# Group by
shipment_GA_grouped = groupBy(shipment_GA_merged)

# normalize
normalize(shipment_GA_grouped)


# Plot
plot(shipment_GA_grouped, 'GA')



############## Diff-in-diff plot (FL, AL, GA) ##################

# Diff-in-diff plot for three states
prePost = (ggplot(aes(x = 'YEAR', y = 'QUANTITY_PERCAP', group = 'POST', color = 'BUYER_STATE'))
           # Florida
           +geom_smooth(method = 'lm', fill = None, data = shipment_FL_grouped)
           # Alabama
           +geom_smooth(method = 'lm', fill = None, data = shipment_AL_grouped)
           # Georgia
           +geom_smooth(method = 'lm', fill = None, data = shipment_GA_grouped)
           # Change themes
           +theme_classic(base_family = "Helvetica")
           # change labels
           +labs(title = "Opioid Shipments Rate, Policy Change in 2010 in FL",
                 x = "Year",
                 y = "Quantity Per Cap",
                 color = "State")
          )
prePost.save(f'/Users/ZifanPeng/Desktop/estimating-impact-of-opioid-prescription-regulations-team-2/30_results/Diff-in-diff.png')

# Diff-in-diff plot for treatment(FL) and control(AL & GA)
# Make all the counties in AL & GA a county pool
shipment_AL_GA = pd.concat([shipment_AL_grouped, shipment_GA_grouped])
prePost2 = (ggplot(aes(x = 'YEAR', y = 'QUANTITY_PERCAP', group = 'POST', color = 'BUYER_STATE'))
           # Florida
           +geom_smooth(method = 'lm', fill = None, data = shipment_FL_grouped)
           # AL & GA
           +geom_smooth(method = 'lm', fill = None,data = shipment_AL_GA)
           # Change themes
           +theme_classic(base_family = "Helvetica")
           # change labels
           +labs(title = "Opioid Shipments Rate, Policy Change in 2010 in FL",
                 x = "Year",
                 y = "Quantity Per Cap",
                 color = "State")
          )
prePost2.save(f'/Users/ZifanPeng/Desktop/estimating-impact-of-opioid-prescription-regulations-team-2/30_results/Diff-in-diff2.png')
