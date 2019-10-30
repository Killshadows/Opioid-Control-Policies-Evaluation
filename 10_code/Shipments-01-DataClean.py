
import pandas as pd
import numpy as np

'''
Read data and subset cols
'''
# read source data
df = pd.read_csv('/Users/ZifanPeng/Desktop/IDS-data/arcos-fl-statewide-itemized.tsv',sep='\t')

# drop unrelated columns and save as IDS-shipment-data-00.csv
df_shipments = df[['TRANSACTION_DATE', 'BUYER_STATE', 'BUYER_COUNTY', 'QUANTITY', 'UNIT','BUYER_ZIP']].copy()
df_shipments.to_csv('/Users/ZifanPeng/Desktop/IDS-data/IDS-shipment-data-00.csv')

# read data: IDS-shipment-data-00.csv
df_shipments = pd.read_csv('/Users/ZifanPeng/Desktop/IDS-data/IDS-shipment-data-00.csv')
df_shipments.head(10)
# drop col0
df_shipments = df_shipments.drop(['Unnamed: 0'], axis = 1)


'''
Deal with NaN values
'''
# Find if some cols has NaN
# UNIT: all NaN
# BUYER-COUNTy: have NaN
print(df_shipments.isnull().any())
print(df_shipments.isnull().all())

# drop UNIT since it is all NaN
df_shipments = df_shipments.drop(['UNIT'], axis = 1)

# find NaN value in BUYER_COUNTY
df_shipments.head()
df_shipments[df_shipments.BUYER_COUNTY.isnull().values==True]

# google 23635 and find that the county name is 'Pinellas'
# replace NaN with 'Pinellas'
df_shipments = df_shipments.replace(np.nan, 'PINELLAS')
df_shipments.head()


'''
Deal with the time: YEAR-MONTH
'''
# Find the datatype of TRANSACTION_DATE ： int
print(df_shipments.dtypes)

# Convert RTANSACTION_DATE to string in order to subset it
df_shipments['TRANSACTION_DATE'] = df_shipments['TRANSACTION_DATE'].astype(str)

# Subset the TRANSACTION_DATE, and get YEAR and Month
df_shipments['YEAR'] = df_shipments['TRANSACTION_DATE'].apply(lambda x: x[-4:])
df_shipments['MONTH'] = df_shipments['TRANSACTION_DATE'].apply(lambda x: x[-8:-6])
df_shipments.head()

# Convert to int, in order to use PeriodIndex
# Create a new col as YYYY-MM
df_shipments['YEAR'] = df_shipments['YEAR'].astype(int)
df_shipments['MONTH'] = df_shipments['MONTH'].astype(int)
df_shipments['TRANSACTION_TIME'] = pd.PeriodIndex(year=df_shipments["YEAR"], month=df_shipments["MONTH"], freq="m")
df_shipments.head()


'''
Save
'''
# Save the data
df_shipments.to_csv('/Users/ZifanPeng/Desktop/IDS-data/IDS-shipment-data-1023.csv')
