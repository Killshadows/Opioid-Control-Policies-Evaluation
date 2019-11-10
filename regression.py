#Difference in Difference Regression 
def DinD(df1,df2):
    merged = pd.concat([df1,df2])
    merged['POLICY'] = (merged.state = 'FL')*1
    results = smf.ols('QUANTITY_PERCAP ~ YEAR + POST + YEAR:POST +POST:POLICY + POLICY:YEAR:POLICY', data=merged).fit()
    hypotheses =  'POST:POLICY-POST-0, POST:YEAR:POLICY-POST:YEAR=0'
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
    return ['level_differencevel','slope_difference']