import pandas as pd
import numpy as np
import math
import time

def MultiLinearRegression(Y_observed,x1,x2):
    
    identity = list()
    for i in range(len(x1)):
        identity.append(1)
    
    X = np.matrix(zip(identity, x1, x2))
    Xt = np.matrix(X.transpose())

    Y = Y_observed
    a = Xt * X

    b = np.linalg.inv(a)

    c = np.dot(X,b)

    d = np.dot(c,Xt)
    
    y_predicted = np.dot(d,Y)
    time.sleep(5)
    return list(np.array(y_predicted)[0])

def poisson(actual,mean):
    p = math.exp(-mean)
    res = (p * math.pow(mean,actual)) / math.factorial(actual)
    return res

def getResult(mean):
    ls = list()
    for i in range(0,10):
        ls.append(poisson(i,mean)*100)
    return ls.index(max(ls))

def predict():
	global season_stats
	for i in season_stats.index:
		if(season_stats['PFTHG'][i] > season_stats['PFTAG'][i]):
			season_stats['PFTR'][i] = 'H'
		elif(season_stats['PFTAG'][i] > season_stats['PFTHG'][i]):
			season_stats['PFTR'][i] = 'A'
		elif(season_stats['PFTHG'][i] == season_stats['PFTAG'][i]):
			season_stats['PFTR'][i] = 'D'

def RunModel():
	global season_stats
	season_stats = pd.read_csv("season_stats.csv")
	season_stats['PFTAG'] = pd.Series(getResult(f) for f in MultiLinearRegression(season_stats['FTAG'],season_stats['AST'],season_stats['AS']))
	season_stats['PFTHG'] = pd.Series(getResult(f) for f in MultiLinearRegression(season_stats['FTHG'],season_stats['HST'],season_stats['HS']))
	season_stats['MHT'] = pd.Series( f for f in MultiLinearRegression(season_stats['FTHG'],season_stats['HST'],season_stats['HS']))
	season_stats['MAT'] = pd.Series( f for f in MultiLinearRegression(season_stats['FTAG'],season_stats['AST'],season_stats['AS']))
	season_stats['PFTR'] = np.nan
	predict()
	season_stats.to_csv("season_stats_m.csv",sep=',',index=False)
	print("MLR model has been fit, ready to show results.")
	print("Enter team from the list for team-wise analysis.")
	teams = ""
	for f in season_stats['HomeTeam'].unique():
		teams = teams + str(f + "|")
	print teams
	
	 















