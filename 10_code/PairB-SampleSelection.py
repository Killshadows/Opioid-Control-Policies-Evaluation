######### README ########

# Plots pre-post graphs for treat states and also all other states
# Runs regressions for pre-trend-line and get estimates
# Compare estimates to select ideal control states

# Start with FL on Nov.8
# Need review before moving forwards

"""
Pre-Post analysis - FL

Plotting Pre-Post Graphs
"""

from plotnine import *

# Change datatype of deaths rate to float
mortality_pop_norm['Deaths_PerCap_County'] = mortality_pop_norm['Deaths_PerCap_County'].astype('float')

# Plot pre-post graphs for FL
mortality_FL = mortality_pop_norm[mortality_pop_norm['State']=='FL']
(ggplot(mortality_FL, aes(x='Year', y='Deaths_PerCap_County')) +
        geom_point(alpha = 0.5) +
        # add pre-trend line and make it red
        geom_smooth(method = 'lm', data = mortality_FL[mortality_FL['Year'] <= 2010], color = 'red') +
        # add post-trend line
        geom_smooth(method = 'lm', data = mortality_FL[mortality_FL['Year'] > 2010], color = 'black') +
        # change labels
        labs(title = "Time Trends of Drug Deaths Rate 2004-2015",
             x = "Time",
             y = "Drug Deaths Rate")
)


"""
Pre-Post analysis - TX

Plotting Pre-Post Graphs
"""



"""
Pre-Post analysis - DC

Plotting Pre-Post Graphs
"""





"""
Choosing Sample for FL

Plotting Pre-Post Graphs for All States
Policy Change in 2010
"""

# Select Sample for FL, where the time change will be 2011

# Plot
(ggplot(mortality_pop_norm, aes(x='Year', y='Deaths_PerCap_County')) +
        # add pre-trend line and make it red
        geom_smooth(method = 'lm', data = mortality_pop_norm[mortality_pop_norm['Year'] <= 2010], color = 'red') +
        # add post-trend line
        geom_smooth(method = 'lm', data = mortality_pop_norm[mortality_pop_norm['Year'] > 2010], color = 'black') +
        # change labels
        labs(title = "Drug Deaths Rate 2004-2015, Policy Change in 2011",
             x = "Time",
             y = "Drug Deaths Rate") +
        facet_wrap('State')
)

# So we will not consider ND, SD, VT and WY as candidates because of incomplete data
# It seems that the graphs only give us a sketchy output
# we should also get estimate of the slope and level by regression


"""
Regressions of Pre-Trends before Policy Change
"""

# Get slopes of pre-trend of all states
import statsmodels as sm
import statsmodels.formula.api as smf

# define function for Group-Wise Linear Regression
def regress(data, yvars, xvars):
    Y = data[yvars]
    X = data[xvars]
    result = smf.ols('Y ~ X', data = data).fit()
    return result.params

# Extract data before 2011
mortality_FL_pre = mortality_pop_norm[mortality_pop_norm['Year']<=2010]
mortality_FL_pre

# Group by state
by_state = mortality_FL_pre.groupby('State')
by_state

# Regress by state to get slopes and levels of pre-trends
FL_sample = by_state.apply(regress, 'Deaths_PerCap_County', 'Year')
FL_sample.columns = ['Level','Slope']

# Centering to FL to get the difference of Level and Slope
FL_sample = FL_sample - FL_sample.loc['FL'].values.squeeze()
# Get absolute value ready for sorting
FL_sample_abs =np.absolute(FL_sample)

# Sort the value by Slope and Level
# The one has the least difference should be our ideal sample
# the output suggests we consider CA, OH and MI...

# Should double check them on other control conditions/
# ex: the location, population magnitude, policy change, etc.
FL_sample_abs.sort_values(by=['Slope','Level'])


"""
D-in-D Analysis - FL
"""
