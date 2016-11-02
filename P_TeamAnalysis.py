#Code for
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import math
team = str
def setTeamStats():
    global team
    global team_stats
    global season_stats
    season_stats = pd.read_csv("season_stats_p.csv")
    temp = pd.DataFrame()
    team_stats = season_stats.loc[(season_stats['HomeTeam'] == team) | (season_stats['AwayTeam'] == team)]
    temp = temp.append(team_stats,ignore_index=True)
    team_stats = temp

def getCumulativePoints(stats):
	alist = stats
	rlist = list()
	sum = 0
	for i in alist:
		sum = sum + i
		rlist.append(sum)
	return rlist

#Get the points list of a team in the given season
def getPointsList(stats):
    global team
    temp = pd.DataFrame()
    temp = temp.append(stats,ignore_index=True)
    plist = list()
    sum = 0
    for i in temp['FTR'].index:
        if((temp['FTR'][i] == 'H') & (temp['HomeTeam'][i] == team) | (temp['FTR'][i] == 'A') & (temp['AwayTeam'][i] == team)):
            plist.append(3)
        elif((temp['FTR'][i] == 'D') & (temp['HomeTeam'][i] == team) | (temp['FTR'][i] == 'D') & (temp['AwayTeam'][i] == team)):
            plist.append(1)
        elif((temp['FTR'][i] == 'A') & (temp['HomeTeam'][i] == team) | (temp['FTR'][i] == 'H') & (temp['AwayTeam'][i] == team)):
            plist.append(0)
    return plist

def getPointsList_Predicted(stats):
	temp = pd.DataFrame()
	temp = temp.append(stats,ignore_index=True)
	plist = list()
	sum = 0
	for i in temp['PFTR'].index:
		if((temp['PFTR'][i] == 'H') & (temp['HomeTeam'][i] == team) | (temp['PFTR'][i] == 'A') & (temp['AwayTeam'][i] == team)):
			plist.append(3)
		elif((temp['PFTR'][i] == 'D') & (temp['HomeTeam'][i] == team) | (temp['PFTR'][i] == 'D') & (temp['AwayTeam'][i] == team)):
			plist.append(1)
		elif((temp['PFTR'][i] == 'A') & (temp['HomeTeam'][i] == team) | (temp['PFTR'][i] == 'H') & (temp['AwayTeam'][i] == team)):
			plist.append(0)
	return plist

def getProbfunc(home_mean,away_mean):
    
    def poisson1(actual,mean):
        p = math.exp(-mean)
        res = (p * math.pow(mean,actual)) / math.factorial(actual)
        return res

    def getResult1(mean):
        ls = list()
        for i in range(0,10):
            ls.append(poisson1(i,mean))
        return ls
    
    probMatrix = [[[] for i in range(10)] for i in range(10)]
    homelist = getResult1(home_mean)
    awaylist = getResult1(away_mean)
    homewin = 0.0
    awaywin = 0.0
    draw = 0.0
    for i in range(len(homelist)):
        for j in range(len(awaylist)):
            probMatrix[i][j] = homelist[i] * awaylist[j]
    for i in range(10):
        for j in range(10):
            if(i==j):
                draw = draw + probMatrix[i][j]
            elif(i>j):
                homewin = homewin + probMatrix[i][j]
            elif(i<j):
                awaywin = awaywin + probMatrix[i][j]
    error = 1-(homewin+awaywin+draw)
    return homewin*100,(draw+error)*100,awaywin*100

#Function to get home stats of a specific team
def getHomeStats(team):
    global season_stats
    stats_h = season_stats.loc[season_stats['HomeTeam'] == team]
    return stats_h

#Function to get away stats of a specific team
def getAwayStats(team):
    global season_stats
    stats_a = season_stats.loc[season_stats['AwayTeam'] == team]
    return stats_a

def getResult(mean):
    ls = list()
    for i in range(0,10):
        ls.append(poisson(i,mean)*100)
    return ls.index(max(ls))

#Function to get results for two means generated through the model
def predict(result):    
    home_mean = result[0]
    away_mean = result[1]
    home_goals =  getResult(home_mean)
    away_goals = getResult(away_mean)
    if(home_goals>away_goals):
        return 'H'
    elif(home_goals<away_goals):
        return 'A'
    elif(home_goals==away_goals):
        return 'D'

def getFinalTeamGoals(team_h,team_a):
    
    global season_stats
    
    stats1 = getHomeStats(team_h)
    a = sum(stats1['FTHG'])/19
    avg_home = sum(season_stats['FTHG'])/len(season_stats['FTHG'])
    att = a/avg_home
    
    stats2 = getAwayStats(team_a)
    b = sum(stats2['FTHG'])/19
    defn = b/avg_home
    
    goals_h = att * defn * avg_home
    
    stats1 = getAwayStats(team_a)
    a = sum(stats1['FTAG'])/19
    avg_away = sum(season_stats['FTAG'])/len(season_stats['FTAG'])
    att = a/avg_away
    
    stats2 = getHomeStats(team_h)
    b = sum(stats2['FTAG'])/19
    defn = b/avg_away
    
    goals_a = att * defn * avg_away
    
    return goals_h,goals_a

def getResultProbabilities():
    df = pd.DataFrame()
    global team_stats
    df['HomeTeam'] = team_stats['HomeTeam']
    df['AwayTeam'] = team_stats['AwayTeam']
    df['Home'] = np.nan
    df['Draw'] = np.nan
    df['Away'] = np.nan
    for i in team_stats.index:
        mean_couple = getFinalTeamGoals(team_stats['HomeTeam'][i],team_stats['AwayTeam'][i])
        a = getProbfunc(mean_couple[0],mean_couple[1])
        df['Home'][i] = a[0]
        df['Draw'][i] = a[1]
        df['Away'][i] = a[2]
    return df

def plotHomeResultProbabilities():
    team_df = getResultProbabilities()
    global team
    global season
    if team == "":
        print("TEAM NOT SPECIFIED")
    season = str(min(season_stats['Year']))+'-'+str(max(season_stats['Year']))
    temp = pd.DataFrame()
    home_df = team_df.loc[team_df['HomeTeam']==team]
    temp = temp.append(home_df,ignore_index=True)
    home_df = temp
    awayteams = home_df['AwayTeam']
    del home_df['HomeTeam'],home_df['AwayTeam']
    y = home_df.index
    home_df.plot(kind='barh', stacked=True)
    plt.yticks(y,awayteams)
    plt.xlim([0,100])
    plt.title('Result probabilities of all the matches played by '+team+' at home in the '+season+' season')
    plt.show()

    
def plotAwayResultProbabilities():
    team_df = getResultProbabilities()
    global team
    global season
    if team == "":
        print("TEAM NOT SPECIFIED")
    season = str(min(season_stats['Year']))+'-'+str(max(season_stats['Year']))
    temp = pd.DataFrame()
    away_df = team_df.loc[team_df['AwayTeam']==team]
    temp = temp.append(away_df,ignore_index=True)
    away_df = temp
    hometeams = away_df['HomeTeam']
    del away_df['HomeTeam'],away_df['AwayTeam']
    y = away_df.index
    away_df.plot(kind='barh', stacked=True)
    plt.yticks(y,hometeams)
    plt.xlim([0,100])
    plt.title('Result probabilities of all the matches played by '+team+' at away in the '+season+' season')
    plt.show()
    
def ShowPerformance():
    global team_stats
    #season = str(min(team_stats['Year']))+'-'+str(max(team_stats['Year']))
    team_stats['CumPts'] = getCumulativePoints(getPointsList(team_stats))
    team_stats['PCumPts'] = getCumulativePoints(getPointsList_Predicted(team_stats))
    team_stats['Date'] = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in team_stats['Date']]
    return team_stats['CumPts'],team_stats['PCumPts'],team_stats['Date']



