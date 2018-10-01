from gensim import utils
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.models import Word2Vec

import numpy as np
import pandas as pd

from random import shuffle

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix

import nltk
from nltk.corpus import stopwords

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from nltk.stem.wordnet import WordNetLemmatizer


###not sure how much of the above I really need

def summarizehostel(hostelname, df):

    if df is not None:
        #just getting some summary statistics for formatting
        temp=[hostelname, round(df['value'].mean(),1), round(df['security'].mean(),1), round(df['location'].mean(),1),
        round(df['facilities'].mean(),1),round(df['staff'].mean(),1),round(df['atmosphere'].mean(),1),
        round(df['cleanliness'].mean(),1)]
    else:
        temp=[hostelname, 'NA', 'NA', 'NA', 'NA','NA','NA','NA']
    return temp

def tokenize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if len(word) < 2:
                continue
            tokens.append(word)
    tokens = [token for token in tokens if not str(token).isnumeric()]
    tokens = [token for token in tokens if not any(char.isdigit() for char in token)]
#    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens


###make prediction on clause
def sentenceprocessing(sentence):

    temp = []

    return temp;

###process at the review level to chunks
def reviewprocessing(review):

    temp = []

    return temp;
