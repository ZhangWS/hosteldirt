from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import prepdata
import makemodel
import reviewprocessing

#Initialize app, add bootstrap to it!
app = Flask(__name__, static_url_path='/static')
Bootstrap(app)

#Here I get a bunch of global variables. They're used a lot
hostellinks, hostelreviews, cleanlabeled = prepdata.readdata()
cityvars = prepdata.getcityvars(hostellinks)
train_data, test_data = makemodel.splitsets(cleanlabeled)

#initiatize the TFIDF model FIRST
#you can probably try it with cleanlabeled instead of just train_data to add
#more instances
logreg = makemodel.maketfidf(train_data)


#Standard home page. 'index.html' is the file in your templates that has the CSS and HTML for your app
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', cityvars=cityvars)

@app.route('/city', methods=['GET', 'POST'])
def city():
    cityname = str(request.form['cityname'])
    hostelnames = hostellinks[ hostellinks['city'] == cityname ]
    return render_template('city.html', cityname=cityname, hostelnames=hostelnames.name.tolist())



#After they submit the survey, the index page redirects to dirt.html where dirt is rendered
@app.route('/dirt', methods=['GET', 'POST'])
def dirt():
    hostelname = str(request.form['hostelname'])

    reviews = hostelreviews[ hostelreviews['name'] == hostelname ]

    #now I really want to do a bunch of preprocessing?
    hostelsummary = reviewprocessing.summarizehostel(hostelname, reviews)

    return render_template('dirt.html', hostelsummary = hostelsummary)


if __name__ == "__main__":
    app.run(debug=True)
