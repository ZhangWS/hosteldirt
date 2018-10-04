###This is the file that contains the work horse that is my training algorithm
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
#import spacy

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

def inittfidf():
    return TfidfVectorizer(min_df=2, tokenizer=tokenize_text, preprocessor=None, stop_words='english')

def fittfidf(df,tf_vect):
    train_data_features = tf_vect.fit_transform(df['sentence'])


    svm = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3,random_state=2046, max_iter=5, tol=None, class_weight='balanced')
    svm = svm.fit(train_data_features, df['cleancontent'])

    return svm

#this takes in test data and preps it for fitting
def maketest(df, svm, tf_vect):
    vader = SentimentIntensityAnalyzer()
    isclean = []
    sentiment = []
    sentwords = []
#    nlp = spacy.load('en', disable=['textcat','ner'])

    for review in df.reviewtext:
        parsed = nltk.tokenize.sent_tokenize(review)

        cleansentiment = 0
        cleancounter = 0
        for sent in parsed:
            sent = str(sent).lower()
            sent = re.sub('\s+', ' ', sent)
            sent = sent.translate(str.maketrans('','',string.punctuation))
            test_data_features = tf_vect.transform([sent])
            test_predictions = svm.predict(test_data_features)

            if test_predictions == 1:
                cleancounter = cleancounter + 1
                ts = vader.polarity_scores(sent)
                cleansentiment = cleansentiment + ts['compound'] #.values.astype(int)

        if cleancounter > 0:
            sentiment.append(cleansentiment)
            sentwords.append(makelabel(cleansentiment))
            isclean.append(1)
        else:
            sentiment.append(np.nan)
            sentwords.append(np.nan)
            isclean.append(0)



    #now that we have a clean count for the reviews, we can do some summarization
    df['isclean'] = isclean
    df['sentiment'] = sentiment
    df['sentword'] = sentwords

    return df

def makelabel(sent):
    if sent > 0.3:
        sentword = ("positive")
    elif sent > -0.3:
        sentword = ("neutral")
    else:
        sentword = ("negative")

    return sentword
