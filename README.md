# hosteldirt
*digging up the hostel reviews that you need to read*
Insight 2018 Remote Program project

*	Created hosteldirt (hosteldirt.site), a curation tool to help travelers find the most informative hostel reviews
*	Scraped 10K Hostelworld reviews from 9 cities and hand-labeled a random sample of 2K reviews at the sentence-level (final dataset size: 8.5K) for topicality
*	Utilized TF-IDF vectorization to train SVM classifier that identifies discussion of hostel sanitation with accuracy > 95% (F1-score 85.3 with balanced recall and precision, validated with 5-fold cross validation)
*	Performed sentiment analysis on tone to proxy for reviewer attitudes about sanitation 
*	Deployed web application using Python, PostgreSQL, git, Flask, and Amazon Web Services

## Versions (in reverse chronological order)
* demo: Final product (2 weeks of development). Web app asks for city location and # of reviews, and returns list of hostels for comparison. Final comparison page returns overview of reviews, tone of reviews, and also relevant review excerpts highlighted with the color of the reviewer's attitude with regard to cleanliness. 
* MVP: Product at end of week 2 (wk 1 of development), web app asks for city location, rating dimension, and returns top-rated hostels for that dimension along with the most positive and most negative review. And yes, the webdesign is straight out of a sleep-deprived tumblr.
* Jupyter Work Process: contains notebooks for scraping and cleaning data

**Demo** was tweaked during week 4 to add in SQL functionality to allow for more flexible IO capabilities (e.g. updating the db with new reviews), though this version still contains the cleaned reviews in CSV form, both the original scraped db and the hand-labeled training set.
