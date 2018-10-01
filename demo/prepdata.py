from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy_utils import *
import pandas as pd

def readdata():

    hostellinks = pd.read_csv('data/hostellinks.csv')
    hostelreviews = pd.read_csv('data/hostelreviews.csv')

    #there are rows where one field is NA because of formatting
    #get rid of them or else training will pitch fits
    cleanlabeled = pd.read_csv('data/cleanlabeled.csv')
    cleanlabeled = cleanlabeled.dropna(axis = 0)

    return hostellinks, hostelreviews, cleanlabeled

def getcityvars(df):
    return df['city'].unique().tolist()
