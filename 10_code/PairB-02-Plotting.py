######### README ########
# Author: Jingyi Wu
# Plots pre-post graphs for treat states
# Plots D-in-D graphs based on three types of control/
# Neighbors, Similar states (pre-trend), and Nation-wide (all other US states)
# Runs D-in-D regressions

# Change datatype of deaths rate to float
mortality_pop_norm['Deaths_PerCap_County'] = mortality_pop_norm['Deaths_PerCap_County'].astype('float')

"""
Plotting Pre-Post Graphs
"""
from plotnine import *

# Define the prepost function to plot pre-post graphs
def prepost(treat, post, fullname):
    mortality_group = mortality_pop_norm[mortality_pop_norm['State']==treat]
    prepost_plot = (ggplot(mortality_group,
            aes(x='Year', y='Deaths_PerCap_County')) +
            geom_point(alpha = 0.5) +
            # add pre-trend line and make it red
            geom_smooth(method = 'lm',
                        data = mortality_group[mortality_group['Year'] < post],
                        color = 'red') +
            # add post-trend line
            geom_smooth(method = 'lm',
                        data = mortality_group[mortality_group['Year'] >= post],
                        color = 'black') +
            # change labels
            labs(title = "Time Trends of Drug Deaths Per Cap, 2004-2015, " + fullname,
                 x = "Time",
                 y = "Drug Deaths Per Cap") +
            scale_x_continuous(breaks=range(2004, 2016), minor_breaks=[])
    )
    prepost_plot.save('/Users/killshadows/Desktop/prepost_' + fullname + '.png')
    return

# Plot for three treat states
prepost("FL", 2010, "Florida")
prepost("TX", 2007, "Texas")
prepost("WA", 2012, "Washington")


"""
D-in-D Plotting
"""
# Define the DinD_Plot function to plot D-in-D graphs
def DinD_Plot(treat, control, control_type, post, fullname, y_axis):
    # Subset data
    if (control_type == 'Neighbors') or (control_type == 'Similar states'):
            mortality_group = (mortality_pop_norm[
            (mortality_pop_norm['State']==treat)|
            (mortality_pop_norm['State']==control[0])|
            (mortality_pop_norm['State']==control[1])|
            (mortality_pop_norm['State']==control[2])|
            (mortality_pop_norm['State']==control[3])|
            (mortality_pop_norm['State']==control[4])])
    else:
        mortality_group = mortality_pop_norm[mortality_pop_norm['State']!='AK']
    # Add dummy variables for post and policy_state
    mortality_group['Post'] = (mortality_group['Year'] >= post)
    mortality_group['Policy_State'] = (mortality_group['State']==treat)
    # Plotting
    DinD_plot = (ggplot(mortality_group,
            aes(x='Year', y='Deaths_PerCap_County', group='Post', color = 'Policy_State')) +
            # add pre and post trend line for FL
            geom_smooth(method = 'lm',
                        data = mortality_group[mortality_group['State']==treat],
                        fill=None) +
            # add pre and post trend line for neighbor
            geom_smooth(method = 'lm',
                        data = mortality_group[mortality_group['State']!=treat],
                        fill=None,
                        linetype='dashed') +
            # change labels
            labs(title = fullname + " vs " + control_type + ": Diff-in-Diff of Drug Deaths Per Cap",
                 x = "Time",
                 y = "Drug Deaths Per Cap",
                 color = 'Policy_State') +
            # add vertical lines
            geom_vline(aes(xintercept= post - 1)) +
            geom_vline(aes(xintercept= post)) +
            # modify legends
            scale_colour_manual(name="Counties in State with Policy Change",
                                values=["red", "grey"],
                                labels = ["True: " + treat , "False: " + control_type + ": " + str(', '.join(control))]) +
            theme(legend_position=(.5, -.05)) +
            # modify ticks of x axis
            scale_x_continuous(breaks=range(2004, 2016),minor_breaks=[]) +
            # modify scale of y axis
            coord_cartesian(ylim = y_axis)
            )
    DinD_plot.save('/Users/killshadows/Desktop/DinD_' + fullname + '_' + control_type + '.png')
    return

# Plot for Florida
FL_neighbor = ['LA', 'MS', 'AL', 'GA', 'SC']
FL_similar = ['IA', 'NC', 'AR', 'MO', 'HI']
DinD_Plot('FL', FL_neighbor, 'Neighbors', 2010, 'Florida', [0.00005,0.0002])
DinD_Plot('FL', FL_similar, 'Similar states', 2010, 'Florida', [0.00005,0.0002])
DinD_Plot('FL', ['all other US states'], 'Nation-wide', 2010, 'Florida', [0.00005,0.0002])

# Plot for Texas
TX_neighbor = ['NM', 'OK', 'AR', 'LA', 'KS']
TX_similar = ['NJ', 'MA', 'IN', 'MS', 'OK']
DinD_Plot('TX', TX_neighbor, 'Neighbors', 2007, 'Texas', [0.00005,0.000225])
DinD_Plot('TX', TX_similar, 'Similar states', 2007, 'Texas', [0.00005,0.000225])
DinD_Plot('TX', ['all other US states'], 'Nation-wide', 2007, 'Texas', [0.00005,0.000225])

# Plot for Washington
WA_neighbor = ['OR', 'ID', 'MT', 'NV', 'WY']
WA_similar = ['IL', 'MI', 'CT', 'CO', 'NC']
DinD_Plot('WA', WA_neighbor, 'Neighbors', 2012, 'Washington', [0.00005,0.000225])
DinD_Plot('WA', WA_similar, 'Similar states', 2012, 'Washington', [0.00005,0.000225])
DinD_Plot('WA', ['all other US states'], 'Nation-wide', 2012, 'Washington', [0.00005,0.000225])


"""
D-in-D Regression
"""
import statsmodels as sm
import statsmodels.formula.api as smf

# Define the DinD_Reg function to run D-in-D regressions
def DinD_Reg(treat, control, control_type, post):
    # Subset data
    if (control_type == 'Neighbors') or (control_type == 'Similar states'):
            mortality_group = (mortality_pop_norm[
            (mortality_pop_norm['State']==treat)|
            (mortality_pop_norm['State']==control[0])|
            (mortality_pop_norm['State']==control[1])|
            (mortality_pop_norm['State']==control[2])|
            (mortality_pop_norm['State']==control[3])|
            (mortality_pop_norm['State']==control[4])])
    else:
        mortality_group = mortality_pop_norm[mortality_pop_norm['State']!='AK']
    # Add dummy variables for post and policy_state
    mortality_group['Post'] = (mortality_group['Year'] >= post)
    mortality_group['Policy_State'] = (mortality_group['State']==treat)
    # Change data type of dummy variables to integer for regression
    mortality_group['Post'] = mortality_group['Post'].astype('int')
    mortality_group['Policy_State'] = mortality_group['Policy_State'].astype('int')
    # Adjust for year
    mortality_group['Year_Adjust'] = mortality_group['Year'] - post
    # Regression
    result = smf.ols("Deaths_PerCap_County ~ Policy_State + Year_Adjust + Year_Adjust:Policy_State + Post + Post:Policy_State + Post:Year_Adjust + Post:Year_Adjust:Policy_State", data = mortality_group).fit()
    return result.summary()

# Regression for Florida
DinD_Reg('FL', FL_neighbor, 'Neighbors', 2010)
DinD_Reg('FL', FL_similar, 'Similar states', 2010)
DinD_Reg('FL', ['all other US states'], 'Nation-wide', 2010)

# Regression for Texas
DinD_Reg('TX', TX_neighbor, 'Neighbors', 2007)
DinD_Reg('TX', TX_similar, 'Similar states', 2007)
DinD_Reg('TX', ['all other US states'], 'Nation-wide', 2007)

# Regression for Washington
DinD_Reg('WA', WA_neighbor, 'Neighbors', 2012)
DinD_Reg('WA', WA_similar, 'Similar states', 2012)
DinD_Reg('WA', ['all other US states'], 'Nation-wide', 2012)
