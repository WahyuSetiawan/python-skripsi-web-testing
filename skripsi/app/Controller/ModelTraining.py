import os

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.forms import UploadFileFeature, UploadFileForm, UploadFileTesting
from app.models import ModelTraining, Setting, TestingData, FeatureList

import skripsi.settings as st

class ModelTrainingController(object):
    """description of class"""

    def index(self, request):
        #assert isinstance(request, HttpRequest)
    
        if request.method == "POST":
            saved = False
            fileForm = UploadFileForm(request.POST, request.FILES)
            print(fileForm.is_valid())

            if fileForm.is_valid():
                imagesave = ModelTraining()
                imagesave.datatraining = fileForm.cleaned_data['datatraining']
                imagesave.save()
                saved = True

        else :
            file = ModelTraining()

        return self.tampilHalaman(request)


    def select(self, request):
        if request.method == "GET" and 'datatrain' in request.GET:
            datatrain = Setting.objects.filter(tag = st.setting_pickle_file)

            if len(datatrain) == 0:
                set = Setting(tag = st.setting_pickle_file, valuedata = request.GET['datatrain'])
                set.save()
            else:
                datatrain[0].valuedata = request.GET['datatrain']
                datatrain[0].save()

        return self.tampilHalaman(request)

    def remove(self, request):
        hapus = False
        dir_path = os.path.dirname(os.path.realpath(__file__))

        if request.method == "GET" and 'datatrain' in request.GET:
            datatrain = ModelTraining.objects.filter(id = request.GET['datatrain'])
            datatrainsetting = Setting.objects.filter(tag = st.setting_pickle_file)
            datatersimpan = None

            if len(datatrainsetting) > 0:
                datatersimpan = datatrainsetting[0].valuedata

            if len(datatrain) > 0 :
                if str(datatrain[0].id) != str(datatersimpan):
                    filepath = "".join([st.MEDIA_ROOT,'/', datatrain[0].datatraining.name])

                    if os.path.exists(filepath) :
                        os.remove(filepath)

                    datatrain[0].delete()
                    hapus = True
                else:
                    hapus = False

        return self.tampilHalaman(request)


    def tampilHalaman(self, request):
        modeltraining = ModelTraining.objects.all()
        idsimpan = Setting.objects.filter(tag = st.setting_pickle_file)
        if len(idsimpan) > 0 :
            datatrain = ModelTraining.objects.filter(id = idsimpan[0].valuedata)

        return render(
            request,
            'app/upload.html',
            locals()
        )



