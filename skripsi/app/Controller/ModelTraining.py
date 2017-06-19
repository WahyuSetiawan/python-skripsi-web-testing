import os

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.forms import UploadFileFeature, UploadFileForm, UploadFileTesting
from app.models import SaveFileForm, setting, testingData, FeatureList
from app.views import setting_pickle_file, setting_feature_list

class ModelTraining(object):
    """description of class"""

    def index(request):
        #assert isinstance(request, HttpRequest)
    
        if request.method == "POST":
            saved = False
            fileForm = UploadFileForm(request.POST, request.FILES)
            print(fileForm.is_valid())

            if fileForm.is_valid():
                imagesave = SaveFileForm()
                imagesave.datatraining = fileForm.cleaned_data['datatraining']
                imagesave.save()
                saved = True

        else :
            file = SaveFileForm()

        gambars = SaveFileForm.objects.all()
        datatrain = setting.objects.filter(tag = setting_pickle_file)

        return render(
            request,
            'app/upload.html',
            locals()
        )

    def select(request):
        if request.method == "GET" and 'datatrain' in request.GET:
            datatrain = setting.objects.filter(tag = setting_pickle_file)

            if len(datatrain) == 0:
                set = setting(tag = setting_pickle_file, valuedata = request.GET['datatrain'])
                set.save()
            else:
                datatrain[0].valuedata = request.GET['datatrain']
                datatrain[0].save()

        gambars = SaveFileForm.objects.all()
        datatrain = setting.objects.filter(tag = setting_pickle_file)

        return render(request, 'app/upload.html', locals())

    def remove(request):
        hapus = False
        dir_path = os.path.dirname(os.path.realpath(__file__))

        if request.method == "GET" and 'datatrain' in request.GET:
            datatrain = SaveFileForm.objects.filter(datatraining = request.GET['datatrain'])

            datatrainsetting = setting.objects.filter(tag = setting_pickle_file)

            if len(datatrainsetting) > 0:
                datatersimpan = datatrainsetting[0].valuedata

            if len(datatrain) > 0 :
                if datatrain[0].datatraining.name != datatersimpan:
                    filepath = "".join([st.MEDIA_ROOT,'/', datatrain[0].datatraining.name])

                    if os.path.exists(filepath) :
                        os.remove(filepath)

                    datatrain[0].delete()
                    hapus = True
                else:
                    hapus = False

        gambars = SaveFileForm.objects.all()
        datatrain = setting.objects.filter(tag = setting_pickle_file)

        return render(request, 'app/upload.html', locals())



