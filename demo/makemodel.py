###This is the file that contains the work horse that is my training algorithm
from gensim import utils
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.models import Word2Vec

import numpy as np
import pandas as pd

from random import shuffle

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords

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

def maketfidf(df):
    tf_vect = TfidfVectorizer(min_df=2, tokenizer=nltk.word_tokenize, preprocessor=None, stop_words='english')
    train_data_features = tf_vect.fit_transform(df['sentence'])

    logreg = linear_model.LogisticRegression(n_jobs=1, C=1e5)
    logreg = logreg.fit(train_data_features, df['cleancontent'])

    return logreg
