#Imports
import pandas as pd
from pandas import DataFrame
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pylab
import os
import inspect
#Defining the directory location of the data files
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/Data/"
mypath = path

#Creating an empty dataframe
big_df = DataFrame()

#Function to read from various files and append the empty dataframe
def read_and_append_dataframe(filename):
    global big_df
    small_df = pd.read_csv(mypath+filename, error_bad_lines=False)
    big_df = big_df.append(small_df, ignore_index=True)
    
#To create a list of files from the given directory
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
files_sort = sorted(onlyfiles)

#Populate the empty dataframe with values from the CSV files in the given path
for f in files_sort:
    read_and_append_dataframe(f)

#To split the date column into day, month and year columns
big_df['Day'] = pd.Series([item.split('-')[0] for item in big_df['Date']])
big_df['Month'] = pd.Series([item.split('-')[1] for item in big_df['Date']])
big_df['Year'] = pd.Series([item.split('-')[2] for item in big_df['Date']])

#To drop the date column
big_df = big_df.drop('Date', 1)

#A function that returns the year in YYYY format
def YearFunc(year):
    y = str(year)
    if(y.startswith('9')):
        return '19'+year
    elif(y.startswith('1') | y.startswith('0')):
        return '20'+year

#To update the Year column with each of its value being in YYYY format
big_df['Year'] = pd.Series(YearFunc(f) for f in big_df['Year'])

#To create a column called Date that stores the date values of each match as a datetime data type
big_df['Date'] = [dt.datetime.strptime(d,'%d-%m-%Y').date() for d in big_df['Day']+'-'+big_df['Month']+'-'+big_df['Year']]
