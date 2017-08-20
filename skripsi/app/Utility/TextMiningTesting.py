import re
import sys
import csv
import math
import os
import pickle

import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer

from pyswarm import pso
from sklearn.externals import joblib

from matplotlib import style

from app.Utility.tfidf import TfIdf

style.use("ggplot")

positive = 'positive'
negative = 'negative'
neutral = 'neutral'

class TrainingData:
    hasilpredict = []

    def __init__(self, tweet, stopword, modeldatatraining, featurefile):
        self.st = open(stopword, 'r')
        self.stopWords = self.getStopWordList(stopword)

        self.ff = open(featurefile, 'r')
        self.feature = self.getFeatureList(self.ff)

        #Read the tweets one by one and process it
        ##inpTweets = csv.reader(open('data/sampleTweets.csv', 'rb'), delimiter=',', quotechar='|')

        csvfile = open(tweet, "r")
        self.inpTweets = csv.reader(csvfile)

        self.modeldata = modeldatatraining

        with open(modeldatatraining, 'rb') as fid:
            self.clf = pickle.load(fid)
            #self.clf = joblib.load(modeldatatraining)

    def getFeatureList(self, featurefile):
        featurelist = {
                positive : [], 
                negative : [],
                neutral : []
            }

        for feature in featurefile:
            featurearray = feature.strip().split(',')
            featurelist[featurearray[1]].append(featurearray[0])

        return featurelist

    #start getStopWordList
    def getStopWordList(self,stopWordListFileName):
        #read the stopwords file and build a list
        stopWords = []
        stopWords.append('AT_USER')
        stopWords.append('URL')

        fp = open(stopWordListFileName, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        fp.close()
        return stopWords
    #end

    #memulai filter tweet
    def processTweet(self,tweet):
        # process the tweets

        # menganti kata kapital menjadi kecil
        tweet = tweet.lower()
    
        # menganti kata https://* dan www.* menjadi url
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)

        # menganti @usename ke AT_USER
        # tweet = re.sub('@[^\s]+','AT_USER',tweet)

        # menghilangkan spasi
        tweet = re.sub('[\s]+', ' ', tweet)

        # menghilangkan hastag
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

        # potong
        tweet = tweet.strip('\'"')

        # menghilangkan kata kata unicode untuk emoticon
        tweet = tweet.encode('ascii', 'ignore').decode('unicode_escape')

        tweet =  re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet)

        myre = re.compile(u'['
                    u'\U0001F300-\U0001F5FF'
                    u'\U0001F600-\U0001F64F'
                    u'\U0001F680-\U0001F6FF'
                    u'\u2600-\u26FF\u2700-\u27BF]+', 
                    re.UNICODE)

        # menghilangkan unicode
        tweet = myre.sub('', tweet)

        # menghilangkan username
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
    
        return tweet
    #akhir

    def preprocessingData(self,tweet, stopwords):

        # mempersiapkan varible pembantu
        featureList = []
        tmpFeature = []

        # mempersiapkan api untuk menjadalankan preprocessing dari tokenizer dan steamming
        nltktokenizer = TweetTokenizer()
        factorysteammer = StemmerFactory()
        stemmer = factorysteammer.create_stemmer()

        #proses tokenizer
        featureList = nltktokenizer.tokenize(tweet)

        # menghilangkan kata stopwords
        for w in featureList:
            if w not in stopwords:
                tmpFeature.append(w)
    
        featureList = tmpFeature
        tmpFeature = []

        # proses steamming perkata agar mendapatkan kata baku
        for w in featureList:
            tmpFeature.append(stemmer.stem(w))

        featureList = tmpFeature
        tmpFeature = []

        return featureList

    # vectorizer
    def TFIDF(self,tweet): 
        vectorizer = TfidfVectorizer(min_df = 5, max_df = 0.8, sublinear_tf = True, use_idf = True)

        tmpTfidf = vectorizer.fit_transform(tweet)

        return tmpTfidf

    def persamaanSVM(self, X):
        return self.clf.predict_log_proba(X)

    def exportModel(self,filename):
        pickle.dump(self.clf, open(filename, 'wb'))

    # run program pemanggilan data
    def run(self):
        tfidfDocument = TfIdf()
        tfidfDocument2 = TfIdf()

        tweets = []
        x1 = []

        tfidfresult = {
            positive : [], 
            negative : [],
            neutral : []
            }

        tfidfweight = {
            positive : [], 
            negative : [],
            neutral : []
            }

        tfidfDocument2.add_document(positive, self.feature[positive])
        tfidfDocument2.add_document(negative, self.feature[negative])
        tfidfDocument2.add_document(neutral, self.feature[neutral])

        a = []

        # start loop
        for i, row in enumerate(self.inpTweets):
            tfidfDocument1 = TfIdf()

            hasil  = []
            sentiment = row[0]
            tweet = row[1]

            #tahap preprocessing
            processedTweet = self.processTweet(tweet)
            featureVector = self.preprocessingData(processedTweet, self.stopWords)
            #tweets.append((tweet,processedTweet, featureVector))
            hasil.append(tweet)
            hasil.append(processedTweet)
            hasil.append(featureVector)

            tweets.append(hasil)

            # tahap binary
            tfidfDocument.add_document(i, featureVector)
            tfidfDocument1.add_document(i, featureVector)

            b = tfidfDocument2.similarities(featureVector)

            tfidfweight[positive].append(tfidfDocument1.similarities(self.feature[positive]))
            tfidfweight[negative].append(tfidfDocument1.similarities(self.feature[negative]))
            tfidfweight[neutral].append(tfidfDocument1.similarities(self.feature[neutral]))

            print(b)

            x = [b[0][1],b[1][1],b[2][1]]

            a.append(x)



        '''
        for i, feature in enumerate(self.feature):
            print("generating tf idf per feature : ", feature)
            print(self.feature[feature])
            tfidfresult[feature] = tfidfDocument.similarities(self.feature[feature])
            
            
            for x in tfidfresult[feature]:
                tfidfweight[feature].append(x[1])
            

            print(tfidfresult[feature])
            print(tfidfweight[feature])

            print('\n\n')
        '''
     
        # merubah ke variable yang bisa diterima oleh svm\
        '''
        for i, row in enumerate(tfidfweight[positive]):
            a = [tfidfresult[positive][i][1],tfidfresult[negative][i][1], tfidfresult[neutral][i][1]]
            x1.append(a)
        '''

        #a = x1
        self.hasilpredict = self.clf.predict(a)

        for (i, value) in enumerate(self.hasilpredict):
            tweets[i].append(self.hasilpredict[i])

        return tweets