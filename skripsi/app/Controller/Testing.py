import os
import collections


from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

import skripsi.settings as st

from app.forms import UploadFileFeature, UploadFileForm, UploadFileTesting
from app.models import SaveFileForm, setting, testingData, FeatureList
from app.views import setting_pickle_file, setting_feature_list

from app.Utility.TextMiningTesting import TrainingData
class Testing(object):
    """description of class"""

    def index(request):
        #assert isinstance(request, HttpRequest)
        saved = False

        if request.method == "POST":
            filetesting = UploadFileTesting(request.POST, request.FILES)

            if filetesting.is_valid():
                testingfilesave = testingData();
                testingfilesave.datatesting = filetesting.cleaned_data['datatesting']
                testingfilesave.save()
                saved = True

                dir_path = os.path.dirname(os.path.realpath(__file__))
                datatrain = setting.objects.filter(tag = setting_pickle_file)[0]
                featurelistfile = setting.objects.filter(tag = setting_feature_list)[0]

                train = TrainingData(
                    "".join([st.MEDIA_ROOT, '/',str(testingfilesave.datatesting)]), 
                    'data/feature_list/id-stopwords.txt',
                    "".join([st.MEDIA_ROOT, '/', str(datatrain.valuedata)]),
                    "".join([st.MEDIA_ROOT, '/',str(featurelistfile.valuedata)]),
                    )
                hasil = train.run()

                arrayhasil = train.hasilpredict
                counterhasil = collections.Counter(arrayhasil)
                print(counterhasil['positive'])

        elif request.method == "GET" and 'datatesting' in request.GET:
            filetesting = request.GET['datatesting']

            dir_path = os.path.dirname(os.path.realpath(__file__))
            datatrain = setting.objects.filter(tag = setting_pickle_file)[0]
            featurelistfile = setting.objects.filter(tag = setting_feature_list)[0]

            train = TrainingData(
                "".join([st.MEDIA_ROOT, '/',str(filetesting)]), 
                'data/feature_list/id-stopwords.txt',
                "".join([st.MEDIA_ROOT, '/', str(datatrain.valuedata)]),
                "".join([st.MEDIA_ROOT, '/',str(featurelistfile.valuedata)]),
                )
            hasil = train.run()

            arrayhasil = train.hasilpredict
            counterhasil = collections.Counter(arrayhasil)
            print(counterhasil['positive'])

        else:
            testignidlesave = testingData()

        return render(request,'app/testing.html', locals())

    def daftarTesting(request):
        filetesting = testingData.objects.all()

        return render(request, 'app/daftartesting.html', locals())

    def hapusTesting(request):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        if request.method == "GET" and 'datatesting' in request.GET:
            hapus = False

            datatesting = testingData.objects.filter(datatesting = request.GET['datatesting'])

            if len(datatesting) > 0 :
                filepath = "".join([st.MEDIA_ROOT,'/',datatesting[0].datatesting.name])

                if os.path.exists(filepath): 
                    os.remove(filepath)

                datatesting[0].delete()

                hapus = True

        filetesting = testingData.objects.all()

        return render(request, 'app/daftartesting.html', locals())