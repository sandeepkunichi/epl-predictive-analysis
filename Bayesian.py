#Code for the Bayesian Model - Using PyMc
#@Author - Sandeep

#Imports
import math
import pymc
import sys
import os
import pandas as pd
import numpy as np

#Preparing the priors and assumptions
def PrepareParameters():
	global df
	global observed_home_goals
	global observed_away_goals
	global who_played_whom
	global num_teams
	global num_games
	global home
	global mu_att
	global mu_def
	global tau_att
	global tau_def
	global atts_star
	global defs_star
	observed_home_goals = [row['FTHG'] for i, row in df.iterrows()]
	observed_away_goals = [row['FTAG'] for i, row in df.iterrows()]
	who_played_whom = [(row['Hg'], row['Ag']) for i,row in df.iterrows()]
	num_teams = len(df.HomeTeam.unique())
	num_games = len(who_played_whom)
	home = pymc.Normal('home', 0, .0001, value=0)
	mu_att = pymc.Normal('mu_att', 0, .0001, value=0)
	mu_def = pymc.Normal('mu_def', 0, .0001, value=0)
	tau_att = pymc.Gamma('tau_att', .1, .1)
	tau_def = pymc.Gamma('tau_def', .1, .1)
	atts_star = pymc.Normal("atts_star", mu=mu_att, tau=tau_att, size=num_teams)
	defs_star = pymc.Normal("defs_star", mu=mu_def, tau=tau_def, size=num_teams)

#Poisson formula
def poisson(actual,mean):
	p = math.exp(-mean)
	res = (p * math.pow(mean,actual)) / math.factorial(actual)
	return res

#Getting PDF using variance (lambda value)    
def getResult(mean):
	ls = list()
	for i in range(10):
		ls.append(poisson(i,mean)*100)
	return ls.index(max(ls))

#Setting the Predicted Full Time Result column
def predict():
	global season_stats
	for i in season_stats.index:
		if(season_stats['PFTHG'][i] > season_stats['PFTAG'][i]):
			season_stats['PFTR'][i] = 'H'
		elif(season_stats['PFTAG'][i] > season_stats['PFTHG'][i]):
			season_stats['PFTR'][i] = 'A'
		elif(season_stats['PFTHG'][i] == season_stats['PFTAG'][i]):
			season_stats['PFTR'][i] = 'D'

#Bayesian Model
def RunModel():
	global season_stats
	global df
	df = pd.read_csv("season_stats.csv")
	season_stats = df
	PrepareParameters()
	@pymc.deterministic
	def atts(atts_star=atts_star):
		atts = atts_star.copy()
		atts = atts - np.mean(atts_star)
		return atts

	@pymc.deterministic
	def defs(defs_star=defs_star):
		defs = defs_star.copy()
		defs = defs - np.mean(defs_star)
		return defs

	@pymc.deterministic
	def home_theta(who_played_whom=who_played_whom, home=home, atts=atts, defs=defs): 
		home_attack = [atts[i[0]] for i in who_played_whom]
		away_defense = [defs[i[1]] for i in who_played_whom]
		try:
			resh = [math.exp(home + home_attack[i] + away_defense[i]) for i in range(num_games)]
		except(OverflowError,UnboundLocalError) as e:
			RunModel()
		return resh

	@pymc.deterministic
	def away_theta(who_played_whom=who_played_whom, atts=atts, defs=defs): 
		away_attack = [atts[i[1]] for i in who_played_whom]
		home_defense = [defs[i[0]] for i in who_played_whom]
		try:
			resa = [math.exp(away_attack[i] + home_defense[i]) for i in range(num_games)]
		except(OverflowError,UnboundLocalError) as e:
			RunModel()
		return resa
	
	home_goals = pymc.Poisson('home_goals', mu=home_theta, value=observed_home_goals, observed=True)
	away_goals = pymc.Poisson('away_goals', mu=away_theta, value=observed_away_goals, observed=True)
	mcmc = pymc.MCMC([home, mu_att, mu_def, tau_att, tau_def, home_theta, away_theta, atts_star, defs_star, atts, defs, home_goals, away_goals])
	map_ = pymc.MAP( mcmc )
	map_.fit()
	result = mcmc.sample(10000,2000,2)

	season_stats['PFTHG'] = [getResult(f) for f in mcmc.trace(home_theta)[:][-1]]
	season_stats['BHT'] = mcmc.trace(home_theta)[:][-1]
	season_stats['PFTAG'] = [getResult(f) for f in mcmc.trace(away_theta)[:][-1]]
	season_stats['BAT'] = mcmc.trace(away_theta)[:][-1]
	season_stats['PFTR'] = np.nan
	predict()
	
	season_stats.to_csv('season_stats_b.csv', sep=',',index=False)

	effects = pd.DataFrame(columns=['Team','AttackEffect','DefenseEffect'])
	effects['Team'] = pd.Series(sorted(season_stats['HomeTeam'].unique()))
	effects['AttackEffect'] = pd.Series(mcmc.trace(atts)[:][-1])
	effects['DefenseEffect'] = pd.Series(mcmc.trace(defs)[:][-1])

	effects.to_csv('effects.csv',sep=',',index=False)

	parameter = pd.DataFrame(columns=['home_theta','home_actual','away_theta','away_actual'])
	parameter['home_theta'] = mcmc.trace(home_theta)[:][-1]
	parameter['home_actual'] = season_stats['FTHG']
	parameter['away_theta'] = mcmc.trace(away_theta)[:][-1]
	parameter['away_actual'] = season_stats['FTAG']

	parameter.to_csv('parameter.csv',sep=',',index=False)

	
	print("Bayesian model has been fit, ready to show results.")
	print("Enter team from the list for team-wise analysis.")
	teams = ""
	for f in season_stats['HomeTeam'].unique():
		teams = teams + str(f + "|")
	print teams
