from sklearn.metrics import r2_score
import operator
import pandas as pd
import matplotlib.pyplot as plt

def getCumulativePoints(stats):
	alist = stats
	rlist = list()
	sum = 0
	for i in alist:
		sum = sum + i
		rlist.append(sum)
	return rlist

def getPointsList_new(team,stats):
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

def getPointsList_Predicted_new(team,stats):
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

def getTotalPts(team):
	global season_stats
	team_stats = pd.DataFrame()
	team_stats = season_stats.loc[(season_stats['HomeTeam'] == team) | (season_stats['AwayTeam'] == team)]
	return getCumulativePoints(getPointsList_new(team,team_stats))[-1]

def getR2(team):
	global season_stats
	team_stats = season_stats.loc[(season_stats['HomeTeam'] == team) | (season_stats['AwayTeam'] == team)]
	team_stats['CumPts'] = getCumulativePoints(getPointsList_new(team,team_stats))
	team_stats['PCumPts'] = getCumulativePoints(getPointsList_Predicted_new(team,team_stats))
	y_true = team_stats['CumPts']
	y_pred = team_stats['PCumPts']
	return r2_score(y_true,y_pred)

def SeasonPerformers(model):
	global season_stats
	fname = "season_stats_"+str(model)+".csv"
	season_stats = pd.read_csv(fname)
	season = str(int(min(season_stats['Year'])))+"-"+str(int(max(season_stats['Year'])))
	teamlist = season_stats['HomeTeam'].unique()
	pointslist = list()
	result = {}
	for team in teamlist:
		result[team] = getTotalPts(team)
	sorted_result = sorted(result.items(), key=operator.itemgetter(1))
	perf = pd.DataFrame()
	perf['Team'] = [sorted_result[i][0] for i in range(20)]
	perf['TotPts'] = [sorted_result[i][1] for i in range(20)]
	perf['R2'] = [getR2(i) for i in perf['Team']]
	xs = perf['R2']
	ys = perf['TotPts']
	labels = perf['Team']
	plt.scatter(xs,ys,color='blue')
	plt.title("Plot to show the model performance for various teams for the "+season+" season")
	for label, x, y in zip(labels,xs,ys):
		plt.annotate(label, xy=(x,y), xytext = (0,0), textcoords = 'offset points', va='bottom',ha='right')
	plt.xlabel('R2')
	plt.ylabel('Total Points')
	plt.xlim([min(xs)-1,1])
	plt.ylim([min(ys)-1,max(ys)+10])
	plt.show()
	
