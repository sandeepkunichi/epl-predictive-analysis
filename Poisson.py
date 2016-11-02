#The Poisson model - Uses Bivariate analysis to predict outcomes
#@Author - Sandeep

#Imports
import math
import pandas as pd


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

#Poisson Model - To get results predictions
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

#Get number of home team goals
def predictHomeGoals(result):
    home_mean = result[0]
    return getResult(home_mean)

#Get number of away team goals
def predictAwayGoals(result):
    away_mean = result[1]
    return getResult(away_mean)

#Results extraction
def RunModel():
    global season_stats
    season_stats = pd.read_csv("season_stats.csv", usecols=['HomeTeam','AwayTeam','FTHG','FTAG','FTR','Date','Year'])
    
    season_stats['PFTR'] = pd.Series(predict(getFinalTeamGoals(season_stats['HomeTeam'][i],season_stats['AwayTeam'][i])) for i in season_stats.index)
    season_stats['PHT'] = pd.Series(getFinalTeamGoals(season_stats['HomeTeam'][i],season_stats['AwayTeam'][i])[0] for i in season_stats.index)
    season_stats['PAT'] = pd.Series(getFinalTeamGoals(season_stats['HomeTeam'][i],season_stats['AwayTeam'][i])[1] for i in season_stats.index)
    season_stats['PFTHG'] = pd.Series(predictHomeGoals(getFinalTeamGoals(season_stats['HomeTeam'][i],season_stats['AwayTeam'][i])) for i in season_stats.index)
    season_stats['PFTAG'] = pd.Series(predictAwayGoals(getFinalTeamGoals(season_stats['HomeTeam'][i],season_stats['AwayTeam'][i])) for i in season_stats.index)
    season_stats.to_csv('season_stats_p.csv', sep=',',index=False)
    print("Poisson model has been fit, ready to show results.")
    print("Enter team from the list for team-wise analysis.")
    teams = ""
    for f in season_stats['HomeTeam'].unique():
        teams = teams + str(f + "|")
    print teams


