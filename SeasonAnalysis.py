#Code for season-wise analysis after model fitting
#@Author - Sandeep
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import pylab
from mpl_toolkits.mplot3d import Axes3D
#Function to get frequency of total goals scored in a season
def getFrequency(goalist):
    rlist = list()
    goalist = list(goalist)
    for i in range(int(max(goalist))):
        rlist.append(goalist.count(i))
    return rlist

#Plotting the home scored goal frequency
def getHomeGoalDist():
    global season_stats
    season_stats = pd.read_csv("season_stats_p.csv", usecols=['HomeTeam','AwayTeam','FTHG','FTAG','FTR','PFTHG','PFTAG','PFTR','Date','Year'])
    season = str(min(season_stats['Year']))+'-'+str(max(season_stats['Year']))   
    a = plt.subplot()
    b = plt.subplot()
    a.plot(range(len(getFrequency(season_stats['FTHG']))),getFrequency(season_stats['FTHG']),color='black',marker='o',linewidth=5)
    b.bar(range(len(getFrequency(season_stats['PFTHG']))),getFrequency(season_stats['PFTHG']),color='green',width=0.1)
    plt.title("Plot to show the distribution of home goals scored in the "+season+" season")
    plt.xlabel("Number of goals")
    plt.ylabel("Frequency")
    plt.ylim([0,max(max(range(len(getFrequency(season_stats['PFTHG'])))),max(getFrequency(season_stats['PFTHG'])))+50])
    plt.xlim(0,8)
    m = plt.scatter(0,0,color='green')
    n = plt.scatter(0,0,color='black')
    plt.legend((m, n), ('Predicted Distribution', 'Observed Distribution'), scatterpoints=1, loc='upper left', ncol=3, fontsize=15)
    plt.show()

#Plotting the away scored goal frequency    
def getAwayGoalDist():
    global season_stats
    season_stats = pd.read_csv("season_stats_p.csv", usecols=['HomeTeam','AwayTeam','FTHG','FTAG','FTR','PFTHG','PFTAG','PFTR','Date','Year'])
    season = str(min(season_stats['Year']))+'-'+str(max(season_stats['Year'])) 
    a = plt.subplot()
    b = plt.subplot()
    a.plot(range(len(getFrequency(season_stats['FTAG']))),getFrequency(season_stats['FTAG']),color='black',marker='o',linewidth=5)
    b.bar(range(len(getFrequency(season_stats['PFTAG']))),getFrequency(season_stats['PFTAG']),color='green',width=0.1)
    plt.title("Plot to show the distribution of away goals scored in the "+season+" season")
    plt.xlabel("Number of goals")
    plt.ylabel("Frequency")
    plt.ylim([0,max(max(range(len(getFrequency(season_stats['PFTAG'])))),max(getFrequency(season_stats['PFTAG'])))+50])
    plt.xlim(0,8)
    m = plt.scatter(0,0,color='green')
    n = plt.scatter(0,0,color='black')
    plt.legend((m, n), ('Predicted Distribution', 'Observed Distribution'), scatterpoints=1, loc='upper left', ncol=3, fontsize=15)
    plt.show()

def plotAtHome():
    #global season_stats
    season_stats = pd.read_csv("season_stats_m.csv", usecols=['HomeTeam','AwayTeam','FTHG','FTAG','FTR','PFTHG','PFTAG','PFTR','Date','Year','HS','HST'])
    season = str(min(season_stats['Year']))+'-'+str(max(season_stats['Year']))


    global season
    fig = pylab.figure()
    ax = Axes3D(fig)

    xvals = season_stats['HS']
    yvals = season_stats['HST']
    zvals = season_stats['FTHG']
    ax.scatter(xvals, yvals, zvals, color='green')

    ax.set_xlabel('Shots Taken')
    ax.set_ylabel('Shots on Target')
    ax.set_zlabel('Goals Scored')

    ax.set_xlim([0,max(xvals)])
    ax.set_ylim([0,max(yvals)])
    ax.set_zlim([0,max(zvals)])
    plt.title("Plot to show the home goals scored based on shots taken and the shots on target for "+season+" season")
    plt.show()

def plotAtAway():

    season_stats = pd.read_csv("season_stats_m.csv", usecols=['HomeTeam','AwayTeam','FTHG','FTAG','FTR','PFTHG','PFTAG','PFTR','Date','Year','AS','AST'])
    season = str(min(season_stats['Year']))+'-'+str(max(season_stats['Year']))
    global season
    fig = pylab.figure()
    ax = Axes3D(fig)

    xvals = season_stats['AS']
    yvals = season_stats['AST']
    zvals = season_stats['FTAG']
    ax.scatter(xvals, yvals, zvals, color='green')

    ax.set_xlabel('Shots Taken')
    ax.set_ylabel('Shots on Target')
    ax.set_zlabel('Goals Scored')

    ax.set_xlim([0,max(xvals)])
    ax.set_ylim([0,max(yvals)])
    ax.set_zlim([0,max(zvals)])
    plt.title("Plot to show the away goals scored based on shots taken and the shots on target for "+season+" season")
    plt.show()

