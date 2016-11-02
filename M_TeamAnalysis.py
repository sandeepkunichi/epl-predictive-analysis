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
    season_stats = pd.read_csv("season_stats_m.csv")
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

def ShowPerformance():
    global team_stats
    #season = str(min(team_stats['Year']))+'-'+str(max(team_stats['Year']))
    team_stats['CumPts'] = getCumulativePoints(getPointsList(team_stats))
    team_stats['PCumPts'] = getCumulativePoints(getPointsList_Predicted(team_stats))
    team_stats['Date'] = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in team_stats['Date']]
    return team_stats['CumPts'],team_stats['PCumPts'],team_stats['Date']



