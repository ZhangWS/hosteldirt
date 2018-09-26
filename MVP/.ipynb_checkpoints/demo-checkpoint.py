from flask import Flask, render_template, request
import requests
import pandas as pd
import re
import ftfy
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#This is the function that outputs recommendations for my app. You'll replace this with your function that takes in the user input and gives the output
def calcSent(myreviews):
    vader = SentimentIntensityAnalyzer()
    myneg = []
    myneu = []
    mypos = []
    mycompound = []

    for review in myreviews:
        snt = vader.polarity_scores(ftfy.fix_text(review))
        myneg.append(snt['neg'])
        myneu.append(snt['neu'])
        mypos.append(snt['pos'])
        mycompound.append(snt['compound'])
    return myneg, myneu, mypos, mycompound

def matchme(mytopfivenames, myhostels):
    t=pd.DataFrame()
    for named in mytopfivenames:
        keyrows = myhostels[myhostels.name.str.contains(named)]
        t=t.append(keyrows, ignore_index=True)
    return t

def findcomment(mykeyrows, mykey):
    if mykey == "top":
        mytemp = mykeyrows.sort_values(by='sentcomp', ascending=False)
    else:
        mytemp = mykeyrows.sort_values(by='sentcomp', ascending=True)
    return mytemp.reviewtext[:1].values

def findlink(myname, mylinks):
    myrow = mylinks[mylinks.name.str.contains(myname)]
    return myrow.url.values

def fixme(mytopfive, mytemp, mylinks):
    t=pd.DataFrame(columns= ['name','url','value','security','location','facilities','staff','atmosphere','cleanliness', 'topcomment', 'worstcomment'])
    for blah in mytopfive.itertuples():
        keyrows = mytemp[mytemp.name.str.contains(blah.name)]
        keylink = findlink(blah.name, mylinks)
        mytopcomment = findcomment(keyrows, "top")
        mybottomcomment = findcomment(keyrows, "bottom")

        if mytopcomment == mybottomcomment:
            mybottomcomment = ["No other comments!"]
    #    temp=pd.DataFrame([])
        t=t.append({'name': blah.name, 'url': keylink, 'value': round(blah.value,ndigits=1), 'security': round(blah.security,ndigits=1),
        'location': round(blah.location,ndigits=1), 'facilities': round(blah.facilities,ndigits=1), 'staff': round(blah.staff,ndigits=1),
        'atmosphere': round(blah.atmosphere,ndigits=1), 'cleanliness': round(blah.cleanliness,ndigits=1), 'topcomment': mytopcomment,
        'worstcomment': mybottomcomment}, ignore_index=True)
    return t

#Initialize app
app = Flask(__name__, static_url_path='/static')

#Standard home page. 'index.html' is the file in your templates that has the CSS and HTML for your app
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


#After they submit the survey, the index page redirects to dirt.html where dirt is rendered
@app.route('/dirt', methods=['GET', 'POST'])
def dirt():

    ###THESE ARE FORM CRITERIA
    #1. user tells us city that they're interested in
    cityname = str(request.form['cityname'])
    #2. user also enters criterion for filtering
    criterion = str(request.form['rating'])
    #3 are we looking for the worst ones or the best ones?
    sortme = str(request.form['sortme'])
    ###END FORM CRITERIA

    #read in data as CSV
    hostels = pd.read_csv('data/hostelreviews-id.csv')
    links = pd.read_csv('data/hostellinks.csv')
        #okay, now we narrow the criteria to figure out which hostels
    #we'll be working with
        #First, by the criteria specified above,
    targethostels = hostels[ hostels.city == cityname ]
    tworeviews = targethostels['name'].value_counts()
    tworeviews =tworeviews[tworeviews > 5].index.tolist()
    targethostels = targethostels[targethostels['name'].isin(tworeviews)]
    print(targethostels)

    #now sort and group by the top specified values
    sorted = targethostels.groupby('name',as_index=False).mean()
    if sortme == 'best':
        sorted = sorted.sort_values(by=[criterion], ascending=False)
    else:
        sorted = sorted.sort_values(by=[criterion])
    tempfive = sorted[:5]
        #subset the relevant hostels in main comment set
    #before performing sentiment analysis and other stuff
    temp = matchme(tempfive.name, targethostels)

        #Now we need to calculate and return some sentiment (yeah!)
    neg,neu,pos,comp = calcSent(temp.reviewtext)
    temp = temp.assign(sentneg=neg, sentneu=neu, sentpos=pos, sentcomp=comp)

        #okay, now we need to consolidate all of the disparate information
    topfive= fixme(tempfive, temp, links)
    return render_template('dirt.html', topfive = topfive, criterion = criterion, cityname=cityname, sortme=sortme)


app.run(debug=True)
