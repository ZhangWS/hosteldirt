import statistics
import numpy as np
import pandas as pd

#This function summarizes the total ratings that hostels in a city got,
#including the average ratings & the number of reviews received

def summarizehostel(df):
    hostelnames = df['name'].unique()

    temp = []
    for name in hostelnames:
        tempreviews = df[df['name'] == name]
        #get summary stuff
        numreviews = len(tempreviews)
        tvalue = round(tempreviews['value'].mean(),1)
        tsecurity = round(tempreviews['security'].mean(),1)
        tlocation = round(tempreviews['location'].mean(),1)
        tfacilities = round(tempreviews['facilities'].mean(),1)
        tstaff = round(tempreviews['staff'].mean(),1)
        tatmosphere = round(tempreviews['atmosphere'].mean(),1)
        tcleanliness = round(tempreviews['cleanliness'].mean(),1)
        avgrating = round(statistics.mean([tvalue,tsecurity,tlocation,tfacilities,tstaff,tatmosphere,tcleanliness]),1)


        temp.append([name,numreviews,avgrating,tvalue,tsecurity,tlocation,tfacilities,tstaff,tatmosphere,tcleanliness])
    temp = sorted(temp, key=lambda x: (x[2],x[9]), reverse=True)
    return temp
