from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy_utils import *
import psycopg2
import pandas as pd


#Read in available data. Currently from CSV, but will be modified to a PostgreSQL db
def readdata():

##this data is updated via code from Python notebooks and should probably be executed once in a while for maximum fidelity
    db = 'hostel'
    username='Natalia'
    engine = create_engine('postgres://%s@localhost/%s'%(username,db))
    q = text('SELECT * from hostellinks')
    hostellinks = pd.DataFrame(engine.execute(q).fetchall())
#    hostellinks = pd.read_csv('data/hostellinks.csv')
#    hostelreviews = pd.read_csv('data/hostelreviews.csv')
    q=text('SELECT * FROM hostelreviews')
    hostelreviews = pd.DataFrame(engine.execute(q).fetchall())


    #there are rows where one field is NA because of formatting
    #get rid of them or else training will pitch fits
#    cleanlabeled = pd.read_csv('data/cleanlabeled.csv')
    q = text('SELECT * from cleanlabeled')
    cleanlabeled = pd.DataFrame(engine.execute(q).fetchall())

    cleanlabeled = cleanlabeled.dropna(axis = 0)

    return hostellinks, hostelreviews, cleanlabeled

#Which cities exist in our database?
def getcityvars(df):
    return df['city'].unique().tolist()
