import pandas as pd
import numpy as np

'''
Import data
'''
# Merge with POP
# 2019-10-29
import pandas as pd
import numpy as np
# Import shipment data
df_shipments = pd.read_csv('/Users/ZifanPeng/Desktop/IDS-data/IDS-shipment-data-01-cleaned.csv', index_col=0)
df_shipments.head()

# Import poplulation dataset for all states and counties
pop = pd.read_excel('/Users/ZifanPeng/Desktop/IDS-data/Population2010_AllCounties.xls')
pop = pop.iloc[6:3229,0:4].copy().reset_index(drop=True)
pop.columns = ['County', 'State', 'Population_2000', 'Population_2010']
pop = pop.drop('Population_2000', axis = 1)
# We find that 2 rows are null, drop them
pop = pop.dropna(how='all')
pop.head()

# Subset population for Florida
pop_FL = pop[pop.State == 'Florida'].reset_index()



'''
Merge the population data to shipment data
'''
# Make the 'County' in two dataset the same format
pop_FL['County'] = pop_FL['County'].str.upper()
pop_FL['County'] = pop_FL['County'].str.replace(' COUNTY', '')
pop_FL = pop_FL.drop('index', axis = 1)
pop_FL.head()

# merge and check
shipment_FL_merged = pd.merge(df_shipments, pop_FL, left_on='BUYER_COUNTY', right_on='County',
                   how='outer' ,validate = 'm:1', indicator=True)
shipment_FL_merged.drop('County', 'State')

# We find that some counties are not 'both' merged, maybe there are some couties with different names
print(shipment_FL_merged[shipment_FL_merged['_merge']=='left_only'].BUYER_COUNTY.unique())
print(shipment_FL_merged[shipment_FL_merged['_merge']=='right_only']['County'].unique())

# In df_shipments, we have: 'SAINT LUCIE' ,'SAINT JOHNS', 'DE SOTO'
# In pop_FL dataset, we have: 'ST. LUCIE', 'ST. JOHNS', 'DESOTO'
# Now, fix it in pop_FL
pop_FL['County'] = pop_FL['County'].replace({'ST. LUCIE': 'SAINT LUCIE',
                                                          'ST. JOHNS': 'SAINT JOHNS',
                                                          'DESOTO': 'DE SOTO'})

# Merge again
shipment_FL_merged = pd.merge(df_shipments, pop_FL, left_on='BUYER_COUNTY', right_on='County',
                   how='outer' ,validate = 'm:1', indicator=True)
# Check if 'both' merged
assert (shipment_FL_merged['_merge']=='both').all()

# Drop unrelated cols
shipment_FL_merged = shipment_FL_merged.drop( ['County', 'State','_merge'], axis = 1)
# Change the col name 'Population_2010' to make it have the same format as others
shipment_FL_merged = shipment_FL_merged.rename(columns={'Population_2010':'POP'})
shipment_FL_merged.head()

# group by 'BUYER_STATE','BUYER_COUNTY', 'YEAR'
shipment_FL_grouped = shipment_FL_merged.groupby(['BUYER_STATE','BUYER_COUNTY', 'YEAR']).agg({'QUANTITY': 'sum', 'POP':'max'})
shipment_FL_grouped = shipment_FL_grouped.reset_index()
shipment_FL_grouped.head()


'''
Normalization for Quantity
'''
# Normalize the quantity
print(shipment_FL_grouped.dtypes)
shipment_FL_grouped['QUANTITY_PERCAP'] = shipment_FL_grouped['QUANTITY']/shipment_FL_grouped['POP']
shipment_FL_grouped['POST'] = (shipment_FL_grouped.YEAR > 2009)*1
shipment_FL_grouped.head()

'''
Save
'''
# Save the dataset
shipment_FL_merged.to_csv('/Users/ZifanPeng/Desktop/IDS-data/IDS-shipment-data-02-withPOP.csv')
