import os

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.forms import UploadFileFeature, UploadFileForm, UploadFileTesting, StopwordsFrom
from app.models import ModelTraining, Setting, TestingData, FeatureList, Stopwords

import skripsi.settings as st

class StopwordsController(object):
    """description of class"""
    def index(self, request):
        pesan = ""
        if request.method == "POST":
            pesan = "simpan|false"
            fileForm = StopwordsFrom(request.POST, request.FILES)

            if fileForm.is_valid():
                featurelist = Stopwords()
                featurelist.stopwords = fileForm.cleaned_data['stopword']
                featurelist.save()
                pesan = "simpan|true"
        else :
            file = Stopwords()

        return self.tampilHalaman(request, pesan)

    def remove(self, request):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        pesan = "hapus|false"
    
        if request.method == "GET" and 'stopwords' in request.GET:
            dataStopwords = Stopwords.objects.filter(id = request.GET['stopwords'])
            dataStopwordsSetting = Setting.objects.filter(tag = st.setting_stopwords_file)
            datatersimpan = None

            if len(dataStopwordsSetting) > 0: 
                datatersimpan = dataStopwordsSetting[0].valuedata
            
            if len(dataStopwords) > 0 :
                if str(dataStopwords[0].id) != str(datatersimpan):
                
                    filepath = "".join([st.MEDIA_ROOT,'/',dataStopwords[0].stopwords.name])

                    if os.path.exists(filepath): 
                        os.remove(filepath)

                    dataStopwords[0].delete()

                    pesan = "hapus|true"
                else:
                    pesan = "hapus|false"

        return self.tampilHalaman(request, pesan)

    def select(self, request):
        pesan = ""
        if request.method == "GET" and 'stopwords' in request.GET:
            datatrain = Setting.objects.filter(tag = st.setting_stopwords_file)

            if len(datatrain) == 0:
                set = Setting(tag = st.setting_stopwords_file, valuedata = request.GET['stopwords'])
                set.save()
            else:
                datatrain[0].valuedata = request.GET['stopwords']
                datatrain[0].save()

        return self.tampilHalaman(request, pesan)

    def tampilHalaman(self, request, pesan):
        if pesan == "simpan|true" :
            saved = True
        if pesan == "simpan|false" :
            saved = False
        if pesan == "hapus|true":
            hapus = True
        if pesan == "hapus|false":
            hapus = False

        stopwords = Stopwords.objects.all()
        idsave = Setting.objects.filter(tag = st.setting_stopwords_file)

        if len(idsave) > 0 :
            datatrain = Stopwords.objects.filter(id = idsave[0].valuedata)
        
        return render(
            request,
            'app/stopwords.html',
            locals()
        )
