import os
import collections


from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

import skripsi.settings as st

from app.forms import UploadFileFeature, UploadFileForm, UploadFileTesting
from app.models import ModelTraining, Setting, TestingData, FeatureList, Stopwords

from app.Utility.TextMiningTesting import TrainingData

class TestingController(object):
    """description of class"""

    def index(self, request):
        #assert isinstance(request, HttpRequest)
        saved = False

        if request.method == "POST":
            filetesting = UploadFileTesting(request.POST, request.FILES)

            if filetesting.is_valid():
                testingfilesave = TestingData();
                testingfilesave.datatesting = filetesting.cleaned_data['datatesting']
                testingfilesave.save()
                saved = True

                dir_path = os.path.dirname(os.path.realpath(__file__))

                idModeltraining = Setting.objects.filter(tag = st.setting_pickle_file)

                if len(idModeltraining) > 0:
                    modeltraining = ModelTraining.objects.filter(id = idModeltraining[0].valuedata)


                idfeaturelist = Setting.objects.filter(tag = st.setting_feature_list)

                if len(idfeaturelist) > 0:
                    featurelist = FeatureList.objects.filter(id = idfeaturelist[0].valuedata)

                idstopwords = Setting.objects.filter(tag = st.setting_stopwords_file)

                if len(idstopwords) > 0:
                    stopwords = Stopwords.objects.filter(id = idstopwords[0].valuedata)

                if len(idstopwords) > 0 and len(idfeaturelist) > 0 and len(idModeltraining) > 0:
                    train = TrainingData(
                        "".join([st.MEDIA_ROOT, '/',str(testingfilesave.datatesting)]), 
                        "".join([st.MEDIA_ROOT, '/', str(stopwords[0].stopwords)]),
                        "".join([st.MEDIA_ROOT, '/', str(modeltraining[0].datatraining)]),
                        "".join([st.MEDIA_ROOT, '/',str(featurelist[0].FeatureList)]),
                        )
                    hasil = train.run()

                    arrayhasil = train.hasilpredict
                    counterhasil = collections.Counter(arrayhasil)

                return render(request,'app/testing.html', locals())
            else:
                return render(request, 'app/testinggagal.html', locals())

        elif request.method == "GET" and 'datatesting' in request.GET:
            datatesting = TestingData.objects.filter(id = request.GET['datatesting'])

            dir_path = os.path.dirname(os.path.realpath(__file__))

            idModeltraining = Setting.objects.filter(tag = st.setting_pickle_file)

            if len(idModeltraining) > 0:
                modeltraining = ModelTraining.objects.filter(id = idModeltraining[0].valuedata)


            idfeaturelist = Setting.objects.filter(tag = st.setting_feature_list)

            if len(idfeaturelist) > 0:
                featurelist = FeatureList.objects.filter(id = idfeaturelist[0].valuedata)

            idstopwords = Setting.objects.filter(tag = st.setting_stopwords_file)

            if len(idstopwords) > 0:
                stopwords = Stopwords.objects.filter(id = idstopwords[0].valuedata)

            if len(idstopwords) > 0 and len(idfeaturelist) > 0 and len(idModeltraining) > 0 and len(datatesting) > 0:
                train = TrainingData(
                    "".join([st.MEDIA_ROOT, '/',str(datatesting[0].datatesting)]), 
                    "".join([st.MEDIA_ROOT, '/', str(stopwords[0].stopwords)]),
                    "".join([st.MEDIA_ROOT, '/', str(modeltraining[0].datatraining)]),
                    "".join([st.MEDIA_ROOT, '/',str(featurelist[0].FeatureList)]),
                    )
                hasil = train.run()

                arrayhasil = train.hasilpredict
                counterhasil = collections.Counter(arrayhasil)

            return render(request,'app/testing.html', locals())

        else:
            testignidlesave = testingData()

        return render(request, 'app/testigngagal.html', locals())

    def daftarTesting(self, request):
        filetesting = TestingData.objects.all()

        return render(request, 'app/daftartesting.html', locals())

    def hapusTesting(self, request):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        if request.method == "GET" and 'datatesting' in request.GET:
            hapus = False

            datatesting = TestingData.objects.filter(id = request.GET['datatesting'])

            if len(datatesting) > 0 :
                filepath = "".join([st.MEDIA_ROOT,'/',datatesting[0].datatesting.name])

                if os.path.exists(filepath): 
                    os.remove(filepath)

                datatesting[0].delete()

                hapus = True
                
        return self.daftarTesting(request)

    def hapusSemuaTesting(self, request):
        testings = TestingData.objects.all()

        for testing in testings:
                filepath = "".join([st.MEDIA_ROOT,'/',testing.datatesting.name])

                if os.path.exists(filepath): 
                    os.remove(filepath)

                testing.delete()

        return self.daftarTesting(request)