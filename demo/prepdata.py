from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy_utils import *
import pandas as pd


#Read in available data. Currently from CSV, but will be modified to a PostgreSQL db
def readdata():

##This may need to be changed in case we want to work with a SQL db instead
##check on how fast SQL queries are versus from pandas

    hostellinks = pd.read_csv('data/hostellinks.csv')
    hostelreviews = pd.read_csv('data/hostelreviews.csv')

    #there are rows where one field is NA because of formatting
    #get rid of them or else training will pitch fits
    cleanlabeled = pd.read_csv('data/cleanlabeled.csv')
    cleanlabeled = cleanlabeled.dropna(axis = 0)

    return hostellinks, hostelreviews, cleanlabeled

#Which cities exist in our database?
def getcityvars(df):
    return len(df['city'].unique().tolist()), df['city'].unique().tolist()
