#Code for displaying parameter statistics from the model's sample set
#@Author - Sandeep

import pandas as pd
import CreateData
import matplotlib.pyplot as plt

#Function to plot the attack and defense effect of all the teams (Team Comparison) 
def plotEffects():
    season = CreateData.season
    effects = pd.read_csv('effects.csv')
    xs = effects['AttackEffect']
    ys = effects['DefenseEffect']
    labels = effects['Team']
    
    plt.scatter(effects['AttackEffect'],effects['DefenseEffect'],color='green')
    for label, x, y in zip(labels, xs, ys):
        plt.annotate(label, xy = (x, y), xytext = (0, 0),textcoords = 'offset points', va = 'bottom', ha = 'left')
    plt.xlabel('Attack Effect')
    plt.ylabel('Defense Effect')
    plt.title("Plot to show the attack and defense effects of the various teams playing in the "+season+" season")
    plt.show()
    
#Function to plot Home Scoring Intensity
def plotHomeTheta():
    season = CreateData.season
    parameter = pd.read_csv('parameter.csv')
    home_actual = parameter['home_actual']
    home_theta = parameter['home_theta']

    a = plt.subplot()
    b = plt.subplot()
    a.plot(range(380),home_theta,color='green')
    b.plot(range(380),home_actual,color='red')
    plt.xlim([0,380])
    plt.ylim([0,8])
    plt.xlabel('Match Number')
    plt.ylabel('Goals Scored')
    m = plt.scatter(0,0,color='green')
    n = plt.scatter(0,0,color='red')
    plt.title("Plot to show the Scoring Intensity vs Goals Scored through the "+season+" season in home games.")
    plt.legend((m, n), ('Predicted Mean (Scoring Intensity)', 'Goals Scored'), scatterpoints=1, loc='upper right', ncol=3, fontsize=10)
    plt.show()

#Function to plot Away Scoring Intensity
def plotAwayTheta():
    season = CreateData.season
    parameter = pd.read_csv('parameter.csv')
    away_actual = parameter['away_actual']
    away_theta = parameter['away_theta']
 
    a = plt.subplot()
    b = plt.subplot()
    a.plot(range(380),away_theta,color='green')
    b.plot(range(380),away_actual,color='red')
    plt.xlim([0,380])
    plt.ylim([0,8])
    plt.xlabel('Match Number')
    plt.ylabel('Goals Scored')
    m = plt.scatter(0,0,color='green')
    n = plt.scatter(0,0,color='red')
    plt.title("Plot to show the Scoring Intensity vs Goals Scored through the "+season+" season in away games.")
    plt.legend((m, n), ('Predicted Mean (Scoring Intensity)', 'Goals Scored'), scatterpoints=1, loc='upper right', ncol=3, fontsize=10)
    plt.show()

