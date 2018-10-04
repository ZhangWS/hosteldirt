from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import prepdata
import makemodel
import reviewprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

app=Flask(__name__, static_url_path='/static')
bootstrap=Bootstrap(app)

#Here I get a bunch of global variables. They're used a lot
hostellinks, hostelreviews, cleanlabeled = prepdata.readdata()
cityvars = prepdata.getcityvars(hostellinks)
train_data, test_data = makemodel.splitsets(cleanlabeled)
tf_vect = makemodel.inittfidf()
svm = makemodel.fittfidf(train_data, tf_vect)

#this model is already trained. All we need to do for each hostel is to
#1. pipeline and preprocess tokenize_text
#2. fit_transform
#3. output

#Standard home page. 'index.html' is the file in your templates that has the CSS and HTML for your app
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', cityvars=cityvars)

@app.route('/city', methods=['GET', 'POST'])
def city():
    cityname = str(request.form['cityname'])
    reviews = hostelreviews[ hostelreviews['city'] == cityname ]
    hostelsummary = reviewprocessing.summarizehostel(reviews)

    return render_template('city.html', cityname=cityname, hostelsummary=hostelsummary)


#After they submit the survey, the index page redirects to dirt.html where dirt is rendered
@app.route('/dirt', methods=['GET', 'POST'])
def dirt():

    #city currently only returns ONE hostel name because I'm not cool enough to do PHPself.
    #Also investigate daniel's method of scrap -> convert -> compare against model -> summarize
    cityname = str(request.form['cityname'])
    cityhostels = hostelreviews[hostelreviews['city'] == cityname]
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

    numhostels = len(hostels_compare)

    reviews_compare = []

    for hostelname in hostels_compare:

        reviews = hostelreviews[ hostelreviews['name'] == hostelname ]
        hostelname = reviews['name'].unique()
        hostelurl = reviews['url'].unique()
        numreviews = len(reviews.index)

        #this needs to provide summary stats on NLP as well as NLP excerpts
        reviews = makemodel.maketest(reviews, svm, tf_vect)

        cleanrevs = reviews[reviews['isclean']==1]
        cleanrevs = cleanrevs.sort_values(by=['date'], ascending = False)
        numclean = len(cleanrevs.index)
        cleanrevs = cleanrevs[:5]

        if numclean > 0:
            sent = cleanrevs[ cleanrevs['sentword'] == 'positive']
            sentnum = len(sent)
            cleanexcerpt = pd.DataFrame({'date':cleanrevs.date, 'sentiment':cleanrevs.sentiment, 'sentword':cleanrevs.sentword, 'review':cleanrevs.reviewtext})
        else:
            avgsent = 0
            sentnum = 0
            cleanexcerpt = []

        reviews_compare.append([hostelname[0], hostelurl[0], numreviews, numclean,sentnum,cleanexcerpt])

    return render_template('dirt.html', summary=reviews_compare)
#    return render_template('dirt.html', hostelname=hostelname, hostelurl=hostelurl,numreviews = numreviews, numclean = numclean, sentnum = sentnum, cleanexcerpt=cleanexcerpt)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
