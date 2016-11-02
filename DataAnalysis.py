#Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Execute DataMunge script
execfile("DataMunge.py")

#Declaring team stats and season stats global data frames
team_stats = pd.DataFrame()
season_stats = pd.DataFrame()

#Season string - global
season = str

#Team string - global
team = str

#Attribute string - global
attr = str

#
def setSeasonStats(s):
    global season
    season = s
    years = season.split('-')
    year1 = years[0]
    year2 = years[1]
    temp = pd.DataFrame()
    global season_stats
    global teamlist
    big_df['Month'] = pd.Series(int(f) for f in big_df['Month'])
    season_stats = big_df.loc[((big_df['Year'] == year1) & (big_df['Month'] >= 8)) | ((big_df['Year'] == year2) & (big_df['Month'] <= 5))]
    temp = temp.append(season_stats,ignore_index=True)
    season_stats = temp

def setTeamStats(team):
    global team_stats
    global season_stats
    global attr
    temp = pd.DataFrame()
    team_stats = season_stats.loc[(season_stats['HomeTeam'] == team) | (season_stats['AwayTeam'] == team)]
    temp = temp.append(team_stats,ignore_index=True)
    team_stats = temp
    lis = list()
    for f in team_stats.columns:
        if(pd.notnull(team_stats[f][0])):
            lis.append(f)
    if 'H'+attr not in lis:
        print("This feature not available for this season. Select another feature.")
    else:
        team_stats = team_stats[lis]

def getCumulativePoints(stats):
	alist = stats
	rlist = list()
	sum = 0
	for i in alist:
		sum = sum + i
		rlist.append(sum)
	return rlist

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

def returnValues():
	global season
	global team
	global attr
	setSeasonStats(season)
	setTeamStats(team)
	home = 'H'+attr
	away = 'A'+attr
	global team_stats
	x = range(38)
	y1 = pd.Series(getCumulativePoints(team_stats[home]))
	y2 = pd.Series(getCumulativePoints(team_stats[away]))
	sizes = [f for f in getCumulativePoints(getPointsList(team_stats))]
	return x,y1,y2,sizes




