
import os

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext

from app.forms import UploadFileFeature
from app.models import FeatureList, Setting

import skripsi.settings as st

class FeatureController(object):
    def index(self, request):
        if request.method == "POST":
            saved = False
            fileForm = UploadFileFeature(request.POST, request.FILES)

            if fileForm.is_valid():
                print("simpan feature list")
                featurelist = FeatureList()
                featurelist.FeatureList = fileForm.cleaned_data['featurefile']
                featurelist.save()
                saved = True
        else :
            file = FeatureList()

        return self.tampilHalaman(request)

    def remove(self, request):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        hapus = False
    
        if request.method == "GET" and 'datafeature' in request.GET:
            datatrain = FeatureList.objects.filter(id = request.GET['datafeature'])
            datafeaturesave = Setting.objects.filter(tag = st.setting_feature_list)
            datatersimpan = None

            if len(datafeaturesave) > 0: 
                datatersimpan = datafeaturesave[0].valuedata

            if len(datatrain) > 0 :
                print(datatrain[0].id)
                print(datatersimpan)
                if str(datatrain[0].id) == str(datatersimpan):
                    hapus = False
                else:
                    filepath = "".join([st.MEDIA_ROOT,'/',datatrain[0].FeatureList.name])

                    if os.path.exists(filepath): 
                        os.remove(filepath)

                    datatrain[0].delete()

                    hapus = True
                    

        return self.tampilHalaman(request)

    def select(self, request):
        if request.method == "GET" and 'datafeature' in request.GET:
            datatrain = Setting.objects.filter(tag = st.setting_feature_list)

            if len(datatrain) == 0:
                set = Setting(tag = st.setting_feature_list, valuedata = request.GET['datafeature'])
                set.save()
            else:
                datatrain[0].valuedata = request.GET['datafeature']
                datatrain[0].save()

        return self.tampilHalaman(request)

    def tampilHalaman(self, request):
        
        features = FeatureList.objects.all()
        idsetting  = Setting.objects.filter(tag = st.setting_feature_list)
        if len(idsetting) > 0 :
            datatrain = FeatureList.objects.filter(id = idsetting[0].valuedata)

        return render(
            request,
            'app/featurelist.html',
            locals()
        )