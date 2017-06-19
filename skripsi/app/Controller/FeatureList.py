
import os

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext

from app.forms import UploadFileFeature
from app.models import FeatureList, setting
from app.views import setting_feature_list

import skripsi.settings as st

class Feature(object):
    def index(request):
        if request.method == "POST":
            saved = False
            fileForm = UploadFileFeature(request.POST, request.FILES)

            if fileForm.is_valid():
                featurelist = FeatureList()
                featurelist.FeatureList = fileForm.cleaned_data['featurefile']
                featurelist.save()
                saved = True
        else :
            file = FeatureList()

        gambars = FeatureList.objects.all()
        datatrain = setting.objects.filter(tag = setting_feature_list)

        return render(
            request,
            'app/featurelist.html',
            locals()
        )

    def remove( request):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        hapus = False
    
        if request.method == "GET" and 'datafeature' in request.GET:
            datatrain = FeatureList.objects.filter(FeatureList = request.GET['datafeature'])
            datafeaturesave = setting.objects.filter(tag = setting_feature_list)
            datatersimpan = ""

            if len(datafeaturesave) > 0: 
                datatersimpan = datafeaturesave[0].valuedata
            
            if len(datatrain) > 0 :
                if datatrain[0].FeatureList.name != datatersimpan:
                
                    filepath = "".join([st.MEDIA_ROOT,'/',datatrain[0].FeatureList.name])

                    if os.path.exists(filepath): 
                        os.remove(filepath)

                    datatrain[0].delete()

                    hapus = True
                else:
                    hapus = False

        gambars = FeatureList.objects.all()
        datatrain = setting.objects.filter(tag = setting_feature_list)

        return render(request, 'app/featurelist.html', locals())

    def select(request):
        if request.method == "GET" and 'datafeature' in request.GET:
            datatrain = setting.objects.filter(tag = setting_feature_list)

            if len(datatrain) == 0:
                set = setting(tag = setting_feature_list, valuedata = request.GET['datafeature'])
                set.save()
            else:
                datatrain[0].valuedata = request.GET['datafeature']
                datatrain[0].save()

        gambars = FeatureList.objects.all()
        datatrain = setting.objects.filter(tag = setting_feature_list)

        return render(request, 'app/featurelist.html', locals())