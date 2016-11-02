import pandas as pd
import math

#Function to get Poisson extrapolation
def poisson(actual,mean):
    p = math.exp(-mean)
    res = (p * math.pow(mean,actual)) / math.factorial(actual)
    return res

#Function to pick most probable outcome goals from Poisson extrapolated values
def getResult(mean):
    ls = list()
    for i in range(0,10):
        ls.append(poisson(i,mean)*100)
    return ls.index(max(ls))

def predict(home_goals,away_goals):
    if(home_goals>away_goals):
        return 'H'
    elif(home_goals<away_goals):
        return 'A'
    elif(home_goals==away_goals):
        return 'D'

def RunModel():
	b_df = pd.read_csv("season_stats_b.csv")
	p_df = pd.read_csv("season_stats_p.csv")
	m_df = pd.read_csv("season_stats_m.csv")
	mydf = b_df
	mydf['HT'] = pd.Series((a+b+c)/3 for a,b,c in zip(b_df['BHT'],p_df['PHT'],m_df['MHT']))
	mydf['AT'] = pd.Series((a+b+c)/3 for a,b,c in zip(b_df['BAT'],p_df['PAT'],m_df['MAT']))
	mydf['FTR'] = b_df['FTR']
	mydf['PFTHG'] = pd.Series(getResult(i) for i in mydf['HT'])
	mydf['PFTAG'] = pd.Series(getResult(i) for i in mydf['AT'])
	mydf['PFTR'] = pd.Series(predict(a,b) for a,b in zip(mydf['PFTHG'],mydf['PFTAG']))
	mydf.to_csv("season_stats_mixed.csv",index=False)
	print("Mixed model has been fit, ready to show results.")
	print("Enter team from the list for team-wise analysis.")
	teams = ""
	for f in mydf['HomeTeam'].unique():
		teams = teams + str(f + "|")
	print teams

