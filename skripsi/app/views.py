"""
Definition of views.
"""
from sys import path

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from .forms import UploadFileForm, UploadFileTesting, UploadFileFeature
from .models import SaveFileForm, setting, testingData, FeatureList

from .TextMiningTesting import *

setting_feature_list = "featurelist"
setting_pickle_file = "datatrain"


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

#'''
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
#'''

'''
method yang digunakan untuk testing data
'''

def testing(request):
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
                "".join([dir_path,'/../media/', str(testingfilesave.datatesting)]), 
                'data/feature_list/id-stopwords.txt',
                "".join([dir_path,'/../media/', str(datatrain.valuedata)]),
                "".join([dir_path,'/../media/', str(featurelistfile.valuedata)]),
                )
            hasil = train.run()
    else:
        testignidlesave = testingData()

    return render(request,'app/testing.html', locals()
)

'''
method yang digunakan untuk data training
'''

def uploaddatatraining(request):
    saved = False
    #assert isinstance(request, HttpRequest)
    
    if request.method == "POST":
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
    datatrain = setting.objects.filter(tag = setting_pickle_file)[0]

    return render(
        request,
        'app/upload.html',
        locals()
    )

def hapusdatatraining(request):
    hapus = False
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if request.method == "GET" and 'datatrain' in request.GET:
        datatrain = SaveFileForm.objects.filter(datatraining = request.GET['datatrain'])

        datatrainsetting = setting.objects.filter(tag = setting_pickle_file)

        if len(datatrainsetting) > 0:
            datatersimpan = datatrainsetting[0].valuedata

        if len(datatrain) > 0 :
            if datatrain[0].datatraining.name != datatersimpan:
                filepath = "".join([dir_path,'/../media/', datatrain[0].datatraining.name])

                if os.path.exists(filepath) :
                    os.remove(filepath)

                datatrain[0].delete()
                hapus = True
            else:
                hapus = False

    gambars = SaveFileForm.objects.all()

    return render(request, 'app/upload.html', locals())


def pilihdatatraining(request):
    
    if request.method == "GET" and 'datatrain' in request.GET:
        datatrain = setting.objects.filter(tag = setting_pickle_file)

        if len(datatrain) == 0:
            set = setting(tag = setting_pickle_file, valuedata = request.GET['datatrain'])
            set.save()
        else:
            datatrain[0].valuedata = request.GET['datatrain']
            datatrain[0].save()

    gambars = SaveFileForm.objects.all()

    return render(request, 'app/upload.html', locals())

'''
method yang diguankan untuk feature
'''

def pilihfeature(request):
    if request.method == "GET" and 'datafeature' in request.GET:
        datatrain = setting.objects.filter(tag = setting_feature_list)

        if len(datatrain) == 0:
            set = setting(tag = setting_feature_list, valuedata = request.GET['datafeature'])
            set.save()
        else:
            datatrain[0].valuedata = request.GET['datafeature']
            datatrain[0].save()

    gambars = FeatureList.objects.all()

    return render(request, 'app/featurelist.html', locals())

def hapusfeature(request):
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
                
                filepath = "".join([dir_path,'/../media/', datatrain[0].FeatureList.name])

                if os.path.exists(filepath): 
                    os.remove(filepath)

                datatrain[0].delete()

                hapus = True
            else:
                hapus = False

    gambars = FeatureList.objects.all()

    return render(request, 'app/featurelist.html', locals())

def feature(request):
    saved = False
    
    if request.method == "POST":
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
    return