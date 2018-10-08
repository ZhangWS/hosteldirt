from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import prepdata
import makemodel
import reviewprocessing
import pandas as pd
import statistics

#initialize application with Bootstrap
app=Flask(__name__, static_url_path='/static')
Bootstrap(app)

#Set a bunch of global variables that are used a lot
hostellinks, hostelreviews, cleanlabeled = prepdata.readdata()
cityvars = prepdata.getcityvars(hostellinks)
train_data, test_data = makemodel.splitsets(cleanlabeled)
tf_vect = makemodel.inittfidf()
svm = makemodel.fittfidf(train_data, tf_vect)

#Standard home page. 'index.html' is the file in your templates that has the CSS and HTML for your app
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', cityvars=cityvars)

#next option to select and compare hostels in one particular city
#remember that you need to provide a passthrough hidden option for the number of reviews requested
@app.route('/city', methods=['GET', 'POST'])
def city():
    cityname = str(request.form['cityname'])
    reqreviews = str(request.form['reqreviews'])

    #create this in prepdata with SQL for more consistency
    reviews = hostelreviews[ hostelreviews['city'] == cityname ]
    numreviews = reviews.shape[0]
    hostelsummary = reviewprocessing.summarizehostel(reviews)
    numhostels = len(hostelsummary)

    return render_template('city.html', cityname=cityname, reqreviews=reqreviews,numhostels=numhostels,numreviews=numreviews,hostelsummary=hostelsummary)

#ALast page provides comparison containing summarized content for all hostels requested
#this function needs refactoring
@app.route('/dirt', methods=['GET', 'POST'])
def dirt():

    #get the two requested variables, city name and # of reviews requested
    cityname = str(request.form['cityname'])
    reqreviews = str(request.form['reqreviews'])

    #assemble a queue of the hostels in that hostel
    #this may be better to do in prepdata, actually, with SQL
    cityhostels = hostelreviews[hostelreviews['city'] == cityname]

    #There are multiple checkboxes, and we need to retrieve the checked values of all of them

    #first, get unique city names (this can be factored and use SQL if need be)
    allhostels = cityhostels['name'].unique().tolist()
    hostels_selected = []
    for i in allhostels:
        if request.form.get(i):
            hostels_selected.append(i)
        else:
            hostels_selected.append('None')

    hostels_compare = []
    for w in range(len(hostels_selected)):
        if hostels_selected[w] !='None':
            hostels_compare.append(hostels_selected[w])

    #hostels_compare is the list of hostels that I need to analyze
    numhostels = len(hostels_compare)

    #these are the reviews, with each row being for a hostel plus selected reviews.
    #this is mostly okay, but we need to institute highlighting for the appropriate row
    reviews_compare = []

    for hostelname in hostels_compare:

        #again, get df of hostel reviews for a particular hostels
        reviews = hostelreviews[ hostelreviews['name'] == hostelname ]
        hostelname = reviews['name'].unique() #unique hostel name
        hostelurl = reviews['url'].unique() #unique url
        numreviews = len(reviews.index) #number of reviews
        rcleanliness = round(reviews['cleanliness'].mean(),1)
        avgrating = round(statistics.mean([reviews['value'].mean(),reviews['security'].mean(),reviews['location'].mean(),reviews['facilities'].mean(),reviews['staff'].mean(),reviews['atmosphere'].mean(),rcleanliness]),1)

        #this needs to provide summary stats on NLP as well as NLP excerpts
        reviews = makemodel.maketest(reviews, svm, tf_vect)

        #get only reviews that are islclean conpliant
        cleanrevs = reviews[reviews['isclean']==1]
        #sort so that newer reviews are at the top
        cleanrevs = cleanrevs.sort_values(by=['date'], ascending = False)
        #figure out how many are clean
        numclean = len(cleanrevs.index)
        #subset only the number requested
        cleanrevs = cleanrevs[:int(reqreviews)]

        if numclean > 0:
            pos = cleanrevs[cleanrevs['sentword'] == 'Positive']
            posnum = len(pos)
            cleanexcerpt = pd.DataFrame({'date':cleanrevs.date, 'sentiment':cleanrevs.sentiment, 'sentword':cleanrevs.sentword, 'reviewtext':cleanrevs.review})
        else:
            posnum = 0
            cleanexcerpt = []

        #appends a list containing multiple parts to it
        reviews_compare.append([hostelname[0], hostelurl[0], numreviews, numclean, posnum, cleanexcerpt, avgrating, rcleanliness])
        #the final thing has got a data frame that's got lists inside
    return render_template('dirt.html', summary=reviews_compare)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
