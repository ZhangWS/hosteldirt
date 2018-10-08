###This is the file that contains the work horse classifier algorithm
from gensim import utils
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.models import Word2Vec

import numpy as np
import pandas as pd

import string
import re

from random import shuffle

from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk

def splitsets(df):
    return train_test_split(df, test_size = 0.2, random_state = 2046)

def tokenize_text(text):
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if len(word) < 2:
                continue
            tokens.append(word)
    tokens = [token for token in tokens if not str(token).isnumeric()]
    tokens = [token for token in tokens if not any(char.isdigit() for char in token)]
    return tokens

#initialize TF-IDF vectorizer. I tried a stopwords version with negation and then also
#the standard Scikit-learn stop list, and there was negligible difference between the stop_words

def inittfidf():
    return TfidfVectorizer(min_df=2, tokenizer=tokenize_text, preprocessor=None, stop_words='english')

#train any sentence on a SVM
def fittfidf(df,tf_vect):
    train_data_features = tf_vect.fit_transform(df['sentence'])

    svm = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3,random_state=2046, max_iter=5, tol=None, class_weight='balanced')
    svm = svm.fit(train_data_features, df['cleancontent'])

    return svm

#this takes in test data and preps it for fitting
def maketest(df, svm, tf_vect):
    vader = SentimentIntensityAnalyzer()
    isclean = []
    sentwords = []
    hreview = []
    hsent = []
    hsentword= []

    for review in df.reviewtext:
        #breakdown to sentence level
        parsed = nltk.tokenize.sent_tokenize(review)

        #for each review, we need to keep track of
        origsentence = [] #parse reviews at sentence level
        cleansentiment = [] #keep track of sentiment score for each sentence
        totsent=0
        cleancounter=0

        for sent in parsed:
            #you want the original in sentence form too for display
            origsentence.append(sent)

            #preprocess and tokenize before generationg prediction
            sent = str(sent).lower()
            sent = re.sub('\s+', ' ', sent)
            sent = sent.translate(str.maketrans('','',string.punctuation))
            test_data_features = tf_vect.transform([sent])
            test_predictions = svm.predict(test_data_features)

            if test_predictions == 1:
                cleancounter = cleancounter + 1 #is this review clean? 0 or #
                tempsent = vader.polarity_scores(sent)
                totsent = totsent + tempsent['compound']
                cleansentiment.append(tempsent['compound'])
            else:
                cleansentiment.append('None') #actually no sentiment (aka this is not a sentence about cleanliness)

        #at the end of the for loop, you should have a list of sentences from the #review
        #and a list of sentiment scores for each sentence that's clean, plus a counter for how many clean sentences there are

        if cleancounter > 0: #after processing ONE review
            # we need to return the two lists, origsentence and cleansentiment
            # we need to return the list isclean, we need to make a label to know general sentiment
            hreview.append(origsentence)
            hsent.append(cleansentiment)
            hsentword.append(makelabel(totsent))
            isclean.append(1)
        else:
            hreview.append(origsentence)
            hsent.append(np.nan)
            hsentword.append('None')
            isclean.append(0)

    #now that we have a clean count for the reviews, we can do some summarization

    df['isclean'] = isclean
    df['review'] = hreview
    df['sentiment'] = hsent
    df['sentword'] = hsentword

    return df

#we want to label the sentiments when we display them
def makelabel(sent):
    if sent > 0.2:
        sentword = ("Positive")
    elif sent > -0.2:
        sentword = ("Neutral")
    else:
        sentword = ("Negative")

    return sentword
