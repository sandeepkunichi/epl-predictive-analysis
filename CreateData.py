#Initialization of Data Cleaning and Processing
#@Author - Sandeep
#Prepare the big dataset (All season-dataset from 1993-2015)
execfile("DataMunge.py")

#Imports
import sys

#Initialize global dataframes for season stats and team stats
season_stats = pd.DataFrame()
team_stats = pd.DataFrame()
season = str
#Setting the season dataframe
def setSeasonStats():
    global season
    years = season.split('-')
    year1 = years[0]
    year2 = years[1]
    if((int(year1) not in range(1993,2016)) | (int(year2) not in range(1993,2016)) | (int(year2)-int(year1)!=1)):
        print("Incorrect season. Enter again.")
    else:
        print("Season statistics have been set for the specified season.")
    temp = pd.DataFrame()
    global season_stats
    global teamlist
    big_df['Month'] = pd.Series(int(f) for f in big_df['Month'])
    season_stats = big_df.loc[((big_df['Year'] == year1) & (big_df['Month'] >= 8)) | ((big_df['Year'] == year2) & (big_df['Month'] <= 5))]
    temp = temp.append(season_stats,ignore_index=True)
    season_stats = temp[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','Year','AST','AS','HST','HS']]
    teamlist = list(season_stats['HomeTeam'].unique())
    teamlist.sort()
    season_stats['Hg'] = pd.Series(teamlist.index(i) for i in season_stats['HomeTeam'])
    season_stats['Ag'] = pd.Series(teamlist.index(i) for i in season_stats['AwayTeam'])
    season_stats.to_csv('season_stats.csv', sep=',',index=False)
       
