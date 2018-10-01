# hosteldirt
*dig up the comment dirt on hostels!*

Insight 2018 Remote Program project

* scraped 10K comments from 900 hostels across 8 cities from Hostelworld with BeautifulSoup in Python
* used NLP to classify whether a comment talks about the cleanliness of the hostel at the sentence level
* Digs up recent, relevant human comments about hostel cleanliness to supplement the official hostel rating when making a decision about where to stay 
* Will be deployed with PostgreSQL Bootstrap, Flask, and AWS when done!

Progress:

* MVP (week 2) - uses canned VADER sentiment analysis (rule-based) - webapp asks for city location, rating dimension, and returns top-rated hostels for that dimension along with the most positive and most negative review. And yes, the webdesign is straight out of a sleep-deprived tumblr.

* Demo version (week 3) - reduced scope to focus on cleanliness. For a desired city, webapp will return a list of hostels along with their cleanliness scores and review excerpts that contain content about sanitation.

* Web app version (week 4) - prettify and make more useful.
