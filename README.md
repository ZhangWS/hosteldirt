# hosteldirt
Insight 2018 Remote Program project

* scraped 10K comments from 900 hostels across 8 cities from Hostelworld.
* Digs up negative comments about cleanliness to let you know how the official hostel rating compares to actual human feedback from the past 90 days.
* Will be deployed with Bootstrap, Flask, and AWS when done!

Progress:

* MVP (week 2) - uses canned VADER sentiment analysis (rule-based) - webapp asks for city location, rating dimension, and returns top-rated hostels for that dimension along with the most positive and most negative review. And yes, the webdesign is straight out of a sleep-deprived tumblr.

* Target demo product (week 3) - reduced scope to focus on cleanliness. For a desired city, webapp will return a list of hostels along with their cleanliness scores and review excerpts that contain content about sanitation. Hopefully, anyways!
