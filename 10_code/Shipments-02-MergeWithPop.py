import pandas as pd
import numpy as np

'''
Import data
'''
# Import shipment data
df_shipments = pd.read_csv('/Users/ZifanPeng/Desktop/IDS-data/IDS-shipment-data-02-cleaned.csv')
df_shipments.head()
# Import population data
pop_FL = pd.read_csv('/Users/ZifanPeng/Desktop/IDS-data/FL-Population-CountyLevel.csv')
pop_FL.head()


'''
Merge the population data to shipment data
'''
# Make the 'County name' in two dataset the same format
pop_FL['County Name'] = pop_FL['County Name'].str.upper()
pop_FL['County Name'] = pop_FL['County Name'].str.replace(' COUNTY', '')
pop_FL = pop_FL.drop(['Growth Rate(from 2010)'], axis = 1)
pop_FL.head()

# merge and check
shipment_FL_merged = pd.merge(df_shipments, pop_FL, left_on='BUYER_COUNTY', right_on='County Name',
                   how='outer' ,validate = 'm:1', indicator=True)

# Some counties are not 'both' merged, maybe there are some couties with different names, check it
print(shipment_FL_merged[shipment_FL_merged['_merge']=='left_only'].BUYER_COUNTY.unique())
print(shipment_FL_merged[shipment_FL_merged['_merge']=='right_only']['County Name'].unique())

# In df_shipments, we have: 'SAINT LUCIE' ,'SAINT JOHNS', 'DE SOTO'
# In pop_FL dataset, we have: 'ST. LUCIE', 'ST. JOHNS', 'DESOTO'
# Now, fix it in pop_FL
pop_FL['County Name'] = pop_FL['County Name'].replace({'ST. LUCIE': 'SAINT LUCIE',
                                                          'ST. JOHNS': 'SAINT JOHNS',
                                                          'DESOTO': 'DE SOTO'})

# Merge again
shipment_FL_merged = pd.merge(df_shipments, pop_FL, left_on='BUYER_COUNTY', right_on='County Name',
                   how='outer' ,validate = 'm:1', indicator=True)
# The two datasets are 'both' merged now
print(shipment_FL_merged['_merge'].unique())


'''
Normalization for Quantity
'''
# Drop unrelated cols
shipment_FL_merged = shipment_FL_merged.drop(['County Name', '_merge'], axis = 1)
# Change the col name 'Population(2019)' to make it have the same format as others
shipment_FL_merged = shipment_FL_merged.rename(columns={'Population(2019)':'POP'})
shipment_FL_merged.head()

# Normalize the quantity
print(shipment_FL_merged.dtypes)
shipment_FL_merged['QUANTITY_PERCAP'] = shipment_FL_merged['QUANTITY']/shipment_FL_merged['POP']
shipment_FL_merged.head()


'''
Save
'''
# Save the dataset
shipment_FL_merged.to_csv('/Users/ZifanPeng/Desktop/IDS-data/IDS-shipment-data-03-withPOP.csv')
