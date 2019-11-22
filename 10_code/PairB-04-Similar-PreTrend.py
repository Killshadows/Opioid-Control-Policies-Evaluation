### ParirB-04-Similar-PreTrend.py
### Author: Shota Takeshima

### Similar trend to FL
Deaths_PreCap_by_State_Year = mortality_pop_norm.groupby(['State', 'Year']).mean()
Deaths_PreCap_by_State_Year

Deaths_PreCap_by_State_Year.reset_index(inplace = True)
Deaths_PreCap_by_State_Year = Deaths_PreCap_by_State_Year[Deaths_PreCap_by_State_Year.Year <= 2009]
Deaths_PreCap_by_State_Year.head(10)


import statsmodels as sm
import statsmodels.formula.api as smf

result = pd.DataFrame(columns = ["State", "Slope", "Level"])

for state in Deaths_PreCap_by_State_Year['State'].unique():
    sub_df = Deaths_PreCap_by_State_Year[Deaths_PreCap_by_State_Year.State == state]
    reg = smf.ols("Deaths_PerCap_County ~ Year", data = sub_df).fit()
    intercept = reg.params[0]
    coef_Year = reg.params[1]
    result = result.append({"State":state, "Slope":coef_Year, "Level":intercept}, ignore_index=True)
    
      
result.set_index('State', inplace = True)
result.sort_values(by = ['Slope', 'Level'])

slope_FL = result.loc['FL', 'Slope']
level_FL = result.loc['FL', 'Level']

result['Slope'] = (result['Slope'] - slope_FL).abs()
result['Level'] = (result['Level'] - level_FL).abs()
result.sort_values(by = ['Slope', 'Level']).iloc[:6, :]


### Similar trend to TX
Deaths_PreCap_by_State_Year = mortality_pop_norm.groupby(['State', 'Year']).mean()
Deaths_PreCap_by_State_Year

Deaths_PreCap_by_State_Year.reset_index(inplace = True)
Deaths_PreCap_by_State_Year = Deaths_PreCap_by_State_Year[Deaths_PreCap_by_State_Year.Year <= 2006]
Deaths_PreCap_by_State_Year.head(10)


result = pd.DataFrame(columns = ["State", "Slope", "Level"])

for state in Deaths_PreCap_by_State_Year['State'].unique():
    sub_df = Deaths_PreCap_by_State_Year[Deaths_PreCap_by_State_Year.State == state]
    reg = smf.ols("Deaths_PerCap_County ~ Year", data = sub_df).fit()
    intercept = reg.params[0]
    coef_Year = reg.params[1]
    result = result.append({"State":state, "Slope":coef_Year, "Level":intercept}, ignore_index=True)
    
      
result.set_index('State', inplace = True)
result.sort_values(by = ['Slope', 'Level'])

slope_TX = result.loc['TX', 'Slope']
level_TX = result.loc['TX', 'Level']

result['Slope'] = (result['Slope'] - slope_TX).abs()
result['Level'] = (result['Level'] - level_TX).abs()
result.sort_values(by = ['Slope', 'Level']).iloc[:6, :]

## Similar trend to Washignton
Deaths_PreCap_by_State_Year = mortality_pop_norm.groupby(['State', 'Year']).mean()
Deaths_PreCap_by_State_Year

Deaths_PreCap_by_State_Year.reset_index(inplace = True)
Deaths_PreCap_by_State_Year = Deaths_PreCap_by_State_Year[Deaths_PreCap_by_State_Year.Year <= 2006]
Deaths_PreCap_by_State_Year.head(10)

result = pd.DataFrame(columns = ["State", "Slope", "Level"])

for state in Deaths_PreCap_by_State_Year['State'].unique():
    sub_df = Deaths_PreCap_by_State_Year[Deaths_PreCap_by_State_Year.State == state]
    reg = smf.ols("Deaths_PerCap_County ~ Year", data = sub_df).fit()
    intercept = reg.params[0]
    coef_Year = reg.params[1]
    result = result.append({"State":state, "Slope":coef_Year, "Level":intercept}, ignore_index=True)
    
      
result.set_index('State', inplace = True)
result.sort_values(by = ['Slope', 'Level'])

slope_WA = result.loc['WA', 'Slope']
level_WA = result.loc['WA', 'Level']

result['Slope'] = (result['Slope'] - slope_WA).abs()
result['Level'] = (result['Level'] - level_WA).abs()
result.sort_values(by = ['Slope', 'Level']).iloc[:6, :]
