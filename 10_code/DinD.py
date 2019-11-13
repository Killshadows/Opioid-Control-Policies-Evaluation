
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
import statsmodels.formula.api as smf


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
    print(prePost)

#Difference in Difference Regression
def DinD(df1,df2,df3):
    merged = pd.concat([df1,df2,df3])
    merged['YEAR'] = merged['YEAR']-2010
    merged['POLICY'] = (merged.BUYER_STATE == 'FL')*1
    results = smf.ols('QUANTITY_PERCAP ~ YEAR + POST + YEAR:POST + POST:POLICY + YEAR:POLICY + POST:YEAR:POLICY', data=merged).fit()
    hypotheses =  'POST:POLICY-POST=0, POST:YEAR:POLICY-YEAR:POST=0'
    t_test = results.t_test(hypotheses)
    print(t_test)


#Select similar trend state
def similar(df1,df2):
    df1_pre = df1[df1['YEAR']<2010]
    df2_pre = df2[df2['YEAR']<2010]
    results1 = smf.ols('QUANTITY_PERCAP ~ YEAR', data=df1_pre).fit()
    results2 = smf.ols('QUANTITY_PERCAP ~ YEAR', data=df2_pre).fit()
    level_difference = results1.params[0]-results2.params[0]
    slope_difference = results1.params[1]-results2.params[1]
    return(level_difference,slope_difference)



####### Import poplulation data ########
# Import poplulation dataset for all states and counties
pop = pd.read_excel('/Users/YuGu/Desktop/team2/00_source/Population2010_AllCounties.xls')
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
shipments_FL = readData('/Users/YuGu/Desktop/690/arcos-fl-statewide-itemized.tsv')
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
shipment_FL_grouped.head()

# Plot
plot(shipment_FL_grouped, 'FL')




###### Alabama ######

# Import shipment data for Alabama
shipments_AL = readData('/Users/YuGu/Desktop/arcos-al-statewide-itemized.tsv')
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
shipment_AL_grouped.head()

# Plot
plot(shipment_AL_grouped, 'AL')






####### Georgia ###########

# Import shipment data for Georgia
shipments_GA = readData('/Users/YuGu/Desktop/arcos-ga-statewide-itemized.tsv')

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
shipment_GA_grouped.head()

# Plot
plot(shipment_GA_grouped, 'GA')


####### Mississippi ###########

# Import shipment data for Georgia
shipments_MS = readData('/Users/YuGu/Desktop/arcos-ms-statewide-itemized.tsv')

# Check if we have nan value
assert (shipments_MS.isnull().any().sum())==0

# Transfer time
shipments_MS = transferDate(shipments_MS)

# Merge shipment data with pop data for GA
# Subset population for MS
pop_MS = pop[pop.State == 'Mississippi'].reset_index().drop('index', axis = 1)
# Merge
shipment_MS_merged = pd.merge(shipments_MS, pop_MS, left_on='BUYER_COUNTY', right_on='County',
                   how='left' ,validate = 'm:1', indicator=True)
# Check if 'both' merged
assert (shipment_MS_merged['_merge']=='both').all()
# Drop uncorrelated cols
shipment_MS_merged = shipment_MS_merged.drop( ['County', 'State','_merge'], axis = 1)

# Group by
shipment_MS_grouped = groupBy(shipment_MS_merged)

# normalize
normalize(shipment_MS_grouped)
shipment_MS_grouped.head()

# Plot
plot(shipment_MS_grouped, 'MS')


####### South Carolina ###########

# Import shipment data for Georgia
shipments_SC = readData('/Users/YuGu/Desktop/arcos-sc-statewide-itemized.tsv')

# Check if we have nan value
assert (shipments_SC.isnull().any().sum())==0

# Transfer time
shipments_SC = transferDate(shipments_SC)

# Merge shipment data with pop data for GA
# Subset population for GA
pop_SC = pop[pop.State == 'South Carolina'].reset_index().drop('index', axis = 1)
# Merge
shipment_SC_merged = pd.merge(shipments_SC, pop_SC, left_on='BUYER_COUNTY', right_on='County',
                   how='left' ,validate = 'm:1', indicator=True)
# Check if 'both' merged
assert (shipment_SC_merged['_merge']=='both').all()
# Drop uncorrelated cols
shipment_SC_merged = shipment_SC_merged.drop( ['County', 'State','_merge'], axis = 1)

# Group by
shipment_SC_grouped = groupBy(shipment_SC_merged)

# normalize
normalize(shipment_SC_grouped)
shipment_SC_grouped.head()

# Plot
plot(shipment_SC_grouped, 'SC')


#######Seek for states with similar trend before policy taking effect

FL_AL = similar(shipment_FL_grouped,shipment_AL_grouped)
FL_GA = similar(shipment_FL_grouped,shipment_GA_grouped)
FL_MS = similar(shipment_FL_grouped,shipment_MS_grouped)
FL_SC = similar(shipment_FL_grouped,shipment_SC_grouped)

trend_compare=pd.DataFrame([FL_AL,FL_GA,FL_MS,FL_SC],columns=['level','slope'])
trend_compare
#AL,MS fits really well with both level and slope. GA's level and slope is a little far, with SC too far. Hence, we will basically do D in D regression on AL and MS.




##########Diff_in_diff regression
DinD = DinD(shipment_FL_grouped,shipment_AL_grouped,shipment_GA_grouped)

##Both insignificant, which suggests there are no level or time trend change
ALGA = pd.concat([shipment_AL_grouped,shipment_GA_grouped])
ALGA['BUYER_STATE'] = 'Control'

############## Diff-in-diff plot (FL, AL, MS) ##################
DinD_graph = (ggplot(aes(x = 'YEAR', y = 'QUANTITY_PERCAP', group = 'POST', color = 'BUYER_STATE'))
           # Florida
           +geom_smooth(method = 'lm', data = shipment_FL_grouped,fill = None)
           # AlMS
           +geom_smooth(method = 'lm', data = ALGA,fill = None)
           # change labels
           +labs(title = "Difference in Differen analysis, Policy Change in 2010 in FL",
                 x = "Year",
                 y = "Quantity Per Cap",
                 color = "BUYER_STATE"))
print(DinD_graph)
DinD_graph.save('/Users/YuGu/Desktop/DinD_graph.png')
