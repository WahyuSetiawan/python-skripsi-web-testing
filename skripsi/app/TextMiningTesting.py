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

style.use("ggplot")

positive = 'positif'
negative = 'negative'
neutral = 'neutral'

class TrainingData:

    def __init__(self, tweet, stopword, modeldatatraining):
        self.st = open(stopword, 'r')
        self.stopWords = self.getStopWordList(stopword)

        #Read the tweets one by one and process it
        ##inpTweets = csv.reader(open('data/sampleTweets.csv', 'rb'), delimiter=',', quotechar='|')

        csvfile = open(tweet, "r")
        self.inpTweets = csv.reader(csvfile)

        self.modeldata = modeldatatraining

        with open(modeldatatraining, 'rb') as fid:
            self.clf = pickle.load(fid)
            #self.clf = joblib.load(modeldatatraining)

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

        tweets = []

        # start loop
        for i, row in enumerate(self.inpTweets):
            sentiment = row[0].replace('|','')
            tweet = row[1].replace('|', '')
            
            #self.list.addItem(''.join(["preprocessing data ke ", str(i)," tweet : ", tweet]))

            #tahap preprocessing
            processedTweet = self.processTweet(tweet)
            featureVector = self.preprocessingData(processedTweet, self.stopWords)
            tweets.append((featureVector, sentiment))

             # tahap binary
            tfidfDocument.add_document(i,featureVector)

            if (sentiment == 'positive' ):
                document['positif'].append(tweet)

                for feature in featureVector:
                    featurelist['positif'].append(feature)

                featurelist['positif'] = list(set(featurelist['positif']))

                label.append(positive)

            if (sentiment == 'negative' ):
                document['negative'].append(tweet)

                for feature in featureVector:
                   featurelist['negative'].append(feature)

                featurelist['negative'] = list(set(featurelist['negative']))

                label.append(negative)

            if (sentiment == 'neutral' ):
                document['neutral'].append(tweet)

                for feature in featureVector:
                   featurelist['neutral'].append(feature)

                featurelist['neutral'] = list(set(featurelist['neutral']))

                label.append(neutral)
        
        # mendapatkan pembobotan menggunakan tf idf
        for i, feature in enumerate(featurelist):
            print("generating tf idf per feature : ", feature)
            tfidfresult[feature] = tfidfDocument.similarities(featurelist[feature])
            
            for x in tfidfresult[feature]:
                tfidfweight[feature].append(x[1])

            print(tfidfresult[feature])
            print(tfidfweight[feature])

            print('\n\n')

     
        # merubah ke variable yang bisa diterima oleh svm
        for i, row in enumerate(tfidfweight[positive]):
            a = [tfidfresult[positive][i][1],tfidfresult[negative][i][1], tfidfresult[neutral][i][1]]

            particle[label[i]].append(a)

            x1.append(a)
    

        for i, x in enumerate(particle):
            print(i)
            print(particle[x])

            lb = []

            for i in particle[x]:
                tmp = []
                for a in i:
                    tmp.append(-1)
                lb.append(tmp)

            print(lb)
            #print(pso(self.persamaanSVM, lb, particle[x]))

        a = x1
        print(self.clf.predict(a))

        ''''
        self.exportModel('modelterbaru.sav')

        self.list.addItem(''.join(['Selesai training model disimpan dalam ', os.path.dirname(__file__) , 'modelterbaru.csv']))

        a = x1
        print(clf.classes_)

        dicision = self.persamaanSVM(a)
        #dicision = clf.predict_proba(a)
        print(dicision)
        print(clf.predict(a))

        #print(clf.predict([10.58,10.76,0.04013377926421405]))
        #print(clf.predict([0, 0.09126984126984126,  1.3140096618357489]))
        #print(clf.get_params())
        w = clf.coef_[0]
        #print(w)

        a = -w[0] / w[1]

        xx = np.linspace(0,12)
        yy = a * xx - clf.intercept_[0] / w[1]

        h0 = plt.plot(xx, yy, 'k-', label="non weighted div")

        #'''

'''
        plt.scatter(X[:, 0], X[:, 1], c = y)
        plt.legend()
        plt.show()



'''




class TfIdf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}

    def add_document(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0

        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])

    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a
list of words.

        """

        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) + (
                      doc_dict[k] / self.corpus_dict[k])
            sims.append([doc[0], score])

        return sims