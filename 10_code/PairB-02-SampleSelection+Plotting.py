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
        geom_smooth(method = 'lm', data = mortality_FL[mortality_FL['Year'] < 2010], color = 'red') +
        # add post-trend line
        geom_smooth(method = 'lm', data = mortality_FL[mortality_FL['Year'] >= 2010], color = 'black') +
        # change labels
        labs(title = "Time Trends of Drug Deaths Per Cap, Florida 2004-2015",
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
D-in-D Analysis
Florida
"""
# Plot pre-post for all states as an overview
p_FL_overview = (ggplot(mortality_pop_norm, aes(x='Year', y='Deaths_PerCap_County')) +
        # add pre-trend line and make it red
        geom_smooth(method = 'lm', data = mortality_pop_norm[mortality_pop_norm['Year'] < 2010], color = 'red') +
        # add post-trend line
        geom_smooth(method = 'lm', data = mortality_pop_norm[mortality_pop_norm['Year'] >= 2010], color = 'black') +
        # change labels
        labs(title = "Drug Deaths Per Cap, All States 2004-2015, Policy Change in 2010",
             x = "Time",
             y = "Drug Deaths Rate") +
        facet_wrap('State')
)
# Save the Plot
p_FL_overview.save('/Users/killshadows/Desktop/project/FL_overview.png')

"""
Florida
2 Neighbors as Control: AL, GA
D-in-D Plotting
"""
# Subset data
mortality_FL_neighbor = (mortality_pop_norm[
    (mortality_pop_norm['State']=='FL')|
    (mortality_pop_norm['State']=='AL')|
    (mortality_pop_norm['State']=='GA')])
# Add dummy variables for post and policy_state
mortality_FL_neighbor['Post'] = (mortality_FL_neighbor['Year']>=2010)
mortality_FL_neighbor['Policy_State'] = (mortality_FL_neighbor['State']=='FL')
# Plotting
p_FL_neighbor = (ggplot(mortality_FL_neighbor, aes(x='Year', y='Deaths_PerCap_County', group='Post', color = 'Policy_State')) +
        # add pre and post trend line for FL
        geom_smooth(method = 'lm', data = mortality_FL_neighbor[mortality_FL_neighbor['State']=='FL'],fill=None) +
        # add pre and post trend line for neighbor
        geom_smooth(method = 'lm', data = mortality_FL_neighbor[mortality_FL_neighbor['State']!='FL'],fill=None,linetype='dashed') +
        # change labels
        labs(title = "Diff-in-Diff, Drug Deaths Per Cap Trends 2004-2015",
             x = "Time",
             y = "Drug Deaths Per Cap",
             color = 'Policy_State') +
        # add vertical lines
        geom_vline(aes(xintercept=2009)) +
        geom_vline(aes(xintercept=2010)) +
        # modify legends
        scale_colour_manual(name="Counties in State with Policy Change", values=["red", "grey"], labels = ["True (Florida)","False (2 Neigbors: AL, GA)"]) +
        theme(legend_position=(.5, -.05)) +
        # modify breaks of x axis
        scale_x_continuous(breaks=range(2004, 2016), minor_breaks=[])
)
p_FL_neighbor.save('/Users/killshadows/Desktop/project/FL_neighbor.png')

"""
Florida
2 Neighbors as Control: AL, GA
D-in-D Regression
"""
# Change data type of dummy variables to integer for regression
mortality_FL_neighbor['Post'] = mortality_FL_neighbor['Post'].astype('int')
mortality_FL_neighbor['Policy_State'] = mortality_FL_neighbor['Policy_State'].astype('int')
# Adjust for year
mortality_FL_neighbor['Year_Adjust'] = mortality_FL_neighbor['Year'] - 2010
# Regression
import statsmodels as sm
import statsmodels.formula.api as smf
result1_FL = smf.ols("Deaths_PerCap_County ~ Year_Adjust + Post + Post:Year_Adjust + Post:Policy_State + Policy_State:Year_Adjust + Post:Year_Adjust:Policy_State", data = mortality_FL_neighbor).fit()
result1_FL.summary()

"""
Florida
All other states as Control
D-in-D Plotting
"""
# Subset data (drop Alaska)
mortality_FL_all = mortality_pop_norm[mortality_pop_norm['State']!='AK']
# Add dummy variables for post and policy_state
mortality_FL_all['Post'] = (mortality_FL_all['Year']>=2010)
mortality_FL_all['Policy_State'] = (mortality_FL_all['State']=='FL')
# Plotting
p_FL_all = (ggplot(mortality_FL_all, aes(x='Year', y='Deaths_PerCap_County', group='Post', color = 'Policy_State')) +
        # add pre and post trend line for FL
        geom_smooth(method = 'lm', data = mortality_FL_all[mortality_FL_all['State']=='FL'],fill=None) +
        # add pre and post trend line for neighbor
        geom_smooth(method = 'lm', data = mortality_FL_all[mortality_FL_all['State']!='FL'],fill=None,linetype='dashed') +
        # change labels
        labs(title = "Diff-in-Diff, Drug Deaths Per Cap Trends 2004-2015",
             x = "Time",
             y = "Drug Deaths Per Cap",
             color = 'Policy_State') +
        # add vertical lines
        geom_vline(aes(xintercept=2009)) +
        geom_vline(aes(xintercept=2010)) +
        # modify legends
        scale_colour_manual(name="Counties in State with Policy Change", values=["red", "grey"], labels = ["True (Florida)","False (All other US states)"]) +
        theme(legend_position=(.5, -.05)) +
        # modify breaks of x axis
        scale_x_continuous(breaks=range(2004, 2016), minor_breaks=[])
)
p_FL_all.save('/Users/killshadows/Desktop/project/FL_all.png')

"""
Florida
All other states as Control
D-in-D Regression
"""
# Change data type of dummy variables to integer for regression
mortality_FL_all['Post'] = mortality_FL_all['Post'].astype('int')
mortality_FL_all['Policy_State'] = mortality_FL_all['Policy_State'].astype('int')
# Adjust for year
mortality_FL_all['Year_Adjust'] = mortality_FL_all['Year'] - 2010
# Regression
result2_FL = smf.ols("Deaths_PerCap_County ~ Year_Adjust + Post + Post:Year_Adjust + Post:Policy_State + Policy_State:Year_Adjust + Post:Year_Adjust:Policy_State", data = mortality_FL_all).fit()
result2_FL.summary()



"""
D-in-D Analysis
Texas
"""
# Plot pre-post for all states as an overview
p_TX_overview = (ggplot(mortality_pop_norm, aes(x='Year', y='Deaths_PerCap_County')) +
        # add pre-trend line and make it red
        geom_smooth(method = 'lm', data = mortality_pop_norm[mortality_pop_norm['Year'] < 2007], color = 'red') +
        # add post-trend line
        geom_smooth(method = 'lm', data = mortality_pop_norm[mortality_pop_norm['Year'] >= 2007], color = 'black') +
        # change labels
        labs(title = "Drug Deaths Per Cap, All States 2004-2015, Policy Change in 2007",
             x = "Time",
             y = "Drug Deaths Rate") +
        facet_wrap('State')
)
p_TX_overview.save('/Users/killshadows/Desktop/project/TX_overview.png')

"""
Texas
4 Neighbors as Control: NM, OK, AR, LA
D-in-D Plotting
"""
# Subset data
mortality_TX_neighbor = (mortality_pop_norm[
    (mortality_pop_norm['State']=='TX')|
    (mortality_pop_norm['State']=='NM')|
    (mortality_pop_norm['State']=='OK')|
    (mortality_pop_norm['State']=='AR')|
    (mortality_pop_norm['State']=='LA')])
# Add dummy variables for post and policy_state
mortality_TX_neighbor['Post'] = (mortality_TX_neighbor['Year']>=2007)
mortality_TX_neighbor['Policy_State'] = (mortality_TX_neighbor['State']=='TX')
# Plotting
p_TX_neighbor = (ggplot(mortality_TX_neighbor, aes(x='Year', y='Deaths_PerCap_County', group='Post', color = 'Policy_State')) +
        # add pre and post trend line for FL
        geom_smooth(method = 'lm', data = mortality_TX_neighbor[mortality_TX_neighbor['State']=='TX'],fill=None) +
        # add pre and post trend line for neighbor
        geom_smooth(method = 'lm', data = mortality_TX_neighbor[mortality_TX_neighbor['State']!='TX'],fill=None,linetype='dashed') +
        # change labels
        labs(title = "Diff-in-Diff, Drug Deaths Per Cap Trends 2004-2015",
             x = "Time",
             y = "Drug Deaths Per Cap",
             color = 'Policy_State') +
        # add vertical lines
        geom_vline(aes(xintercept=2006)) +
        geom_vline(aes(xintercept=2007)) +
        # modify legends
        scale_colour_manual(name="Counties in State with Policy Change", values=["red", "grey"], labels = ["True (Texas)","False (4 Neigbors: NM, OK, AR, LA)"]) +
        theme(legend_position=(.5, -.05)) +
        # modify breaks of x axis
        scale_x_continuous(breaks=range(2004, 2016), minor_breaks=[])
)
p_TX_neighbor.save('/Users/killshadows/Desktop/project/TX_neighbor.png')

"""
Texas
4 Neighbors as Control: NM, OK, AR, LA
D-in-D Regression
"""
# Change data type of dummy variables to integer for regression
mortality_TX_neighbor['Post'] = mortality_TX_neighbor['Post'].astype('int')
mortality_TX_neighbor['Policy_State'] = mortality_TX_neighbor['Policy_State'].astype('int')
# Adjust for year
mortality_TX_neighbor['Year_Adjust'] = mortality_TX_neighbor['Year'] - 2007
# Regression
result1_TX = smf.ols("Deaths_PerCap_County ~ Year_Adjust + Post + Post:Year_Adjust + Post:Policy_State + Policy_State:Year_Adjust + Post:Year_Adjust:Policy_State", data = mortality_TX_neighbor).fit()
result1_TX.summary()

"""
Texas
All other states as Control
D-in-D Plotting
"""
# Subset data (drop Alaska)
mortality_TX_all = mortality_pop_norm[mortality_pop_norm['State']!='AK']
# Add dummy variables for post and policy_state
mortality_TX_all['Post'] = (mortality_TX_all['Year']>=2007)
mortality_TX_all['Policy_State'] = (mortality_TX_all['State']=='TX')
# Plotting
p_TX_all = (ggplot(mortality_TX_all, aes(x='Year', y='Deaths_PerCap_County', group='Post', color = 'Policy_State')) +
        # add pre and post trend line for FL
        geom_smooth(method = 'lm', data = mortality_TX_all[mortality_TX_all['State']=='TX'],fill=None) +
        # add pre and post trend line for neighbor
        geom_smooth(method = 'lm', data = mortality_TX_all[mortality_TX_all['State']!='TX'],fill=None,linetype='dashed') +
        # change labels
        labs(title = "Diff-in-Diff, Drug Deaths Per Cap Trends 2004-2015",
             x = "Time",
             y = "Drug Deaths Per Cap",
             color = 'Policy_State') +
        # add vertical lines
        geom_vline(aes(xintercept=2006)) +
        geom_vline(aes(xintercept=2007)) +
        # modify legends
        scale_colour_manual(name="Counties in State with Policy Change", values=["red", "grey"], labels = ["True (Texas)","False (All other US states)"]) +
        theme(legend_position=(.5, -.05)) +
        # modify breaks of x axis
        scale_x_continuous(breaks=range(2004, 2016), minor_breaks=[])
)
p_TX_all.save('/Users/killshadows/Desktop/project/TX_all.png')

"""
Texas
All other states as Control
D-in-D Regression
"""
# Change data type of dummy variables to integer for regression
mortality_TX_all['Post'] = mortality_TX_all['Post'].astype('int')
mortality_TX_all['Policy_State'] = mortality_TX_all['Policy_State'].astype('int')
# Adjust for year
mortality_TX_all['Year_Adjust'] = mortality_TX_all['Year'] - 2007
# Regression
result2_TX = smf.ols("Deaths_PerCap_County ~ Year_Adjust + Post + Post:Year_Adjust + Post:Policy_State + Policy_State:Year_Adjust + Post:Year_Adjust:Policy_State", data = mortality_TX_all).fit()
result2_TX.summary()



"""
D-in-D Analysis
Washington
"""
# Plot pre-post for all states as an overview
p_WA_overview = (ggplot(mortality_pop_norm, aes(x='Year', y='Deaths_PerCap_County')) +
        # add pre-trend line and make it red
        geom_smooth(method = 'lm', data = mortality_pop_norm[mortality_pop_norm['Year'] < 2012], color = 'red') +
        # add post-trend line
        geom_smooth(method = 'lm', data = mortality_pop_norm[mortality_pop_norm['Year'] >= 2012], color = 'black') +
        # change labels
        labs(title = "Drug Deaths Per Cap, All States 2004-2015, Policy Change in 2012",
             x = "Time",
             y = "Drug Deaths Rate") +
        facet_wrap('State')
)
p_WA_overview.save('/Users/killshadows/Desktop/project/WA_overview.png')

"""
Washington
2 Neighbors as Control: OR, ID
D-in-D Plotting
"""
# Subset data
mortality_WA_neighbor = (mortality_pop_norm[
    (mortality_pop_norm['State']=='WA')|
    (mortality_pop_norm['State']=='OR')|
    (mortality_pop_norm['State']=='ID')])
# Add dummy variables for post and policy_state
mortality_WA_neighbor['Post'] = (mortality_WA_neighbor['Year']>=2012)
mortality_WA_neighbor['Policy_State'] = (mortality_WA_neighbor['State']=='WA')
# Plotting
p_WA_neighbor = (ggplot(mortality_WA_neighbor, aes(x='Year', y='Deaths_PerCap_County', group='Post', color = 'Policy_State')) +
        # add pre and post trend line for FL
        geom_smooth(method = 'lm', data = mortality_WA_neighbor[mortality_WA_neighbor['State']=='WA'],fill=None) +
        # add pre and post trend line for neighbor
        geom_smooth(method = 'lm', data = mortality_WA_neighbor[mortality_WA_neighbor['State']!='WA'],fill=None,linetype='dashed') +
        # change labels
        labs(title = "Diff-in-Diff, Drug Deaths Per Cap Trends 2004-2015",
             x = "Time",
             y = "Drug Deaths Per Cap",
             color = 'Policy_State') +
        # add vertical lines
        geom_vline(aes(xintercept=2011)) +
        geom_vline(aes(xintercept=2012)) +
        # modify legends
        scale_colour_manual(name="Counties in State with Policy Change", values=["red", "grey"], labels = ["True (Washington)","False (2 Neigbors: OR, ID)"]) +
        theme(legend_position=(.5, -.05)) +
        # modify breaks of x axis
        scale_x_continuous(breaks=range(2004, 2016), minor_breaks=[])
)
p_WA_neighbor.save('/Users/killshadows/Desktop/project/WA_neighbor.png')

"""
Washington
2 Neighbors as Control: OR, ID
D-in-D Regression
"""
# Change data type of dummy variables to integer for regression
mortality_WA_neighbor['Post'] = mortality_WA_neighbor['Post'].astype('int')
mortality_WA_neighbor['Policy_State'] = mortality_WA_neighbor['Policy_State'].astype('int')
# Adjust for year
mortality_WA_neighbor['Year_Adjust'] = mortality_WA_neighbor['Year'] - 2012
# Regression
result1_WA = smf.ols("Deaths_PerCap_County ~ Year_Adjust + Post + Post:Year_Adjust + Post:Policy_State + Policy_State:Year_Adjust + Post:Year_Adjust:Policy_State", data = mortality_WA_neighbor).fit()
result1_WA.summary()

"""
Washington
All other states as Control
D-in-D Plotting
"""
# Subset data (drop Alaska)
mortality_WA_all = mortality_pop_norm[mortality_pop_norm['State']!='AK']
# Add dummy variables for post and policy_state
mortality_WA_all['Post'] = (mortality_WA_all['Year']>=2012)
mortality_WA_all['Policy_State'] = (mortality_WA_all['State']=='WA')
# Plotting
p_WA_all = (ggplot(mortality_WA_all, aes(x='Year', y='Deaths_PerCap_County', group='Post', color = 'Policy_State')) +
        # add pre and post trend line for FL
        geom_smooth(method = 'lm', data = mortality_WA_all[mortality_WA_all['State']=='WA'],fill=None) +
        # add pre and post trend line for neighbor
        geom_smooth(method = 'lm', data = mortality_WA_all[mortality_WA_all['State']!='WA'],fill=None,linetype='dashed') +
        # change labels
        labs(title = "Diff-in-Diff, Drug Deaths Per Cap Trends 2004-2015",
             x = "Time",
             y = "Drug Deaths Per Cap",
             color = 'Policy_State') +
        # add vertical lines
        geom_vline(aes(xintercept=2011)) +
        geom_vline(aes(xintercept=2012)) +
        # modify legends
        scale_colour_manual(name="Counties in State with Policy Change", values=["red", "grey"], labels = ["True (Washington)","False (2 Neigbors: OR, ID)"]) +
        theme(legend_position=(.5, -.05)) +
        # modify breaks of x axis
        scale_x_continuous(breaks=range(2004, 2016), minor_breaks=[])
)
p_WA_all.save('/Users/killshadows/Desktop/project/WA_all.png')

"""
Washington
All other states as Control
D-in-D Regression
"""
# Change data type of dummy variables to integer for regression
mortality_WA_all['Post'] = mortality_WA_all['Post'].astype('int')
mortality_WA_all['Policy_State'] = mortality_WA_all['Policy_State'].astype('int')
# Adjust for year
mortality_WA_all['Year_Adjust'] = mortality_WA_all['Year'] - 2012
# Regression
result2_WA = smf.ols("Deaths_PerCap_County ~ Year_Adjust + Post + Post:Year_Adjust + Post:Policy_State + Policy_State:Year_Adjust + Post:Year_Adjust:Policy_State", data = mortality_WA_all).fit()
result2_WA.summary()
