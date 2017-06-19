"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.forms import UploadFileForm, UploadFileTesting, UploadFileFeature
from app.models import SaveFileForm, setting, testingData, FeatureList

from app.Utility.TextMiningTesting import *

setting_feature_list = "featurelist"
setting_pickle_file = "datatrain"

from app.Controller.FeatureList import Feature
from app.Controller.ModelTraining import ModelTraining
from app.Controller.Testing import Testing

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

def testing(request): return Testing().index(request)
def daftartesting(request): return Testing().daftarTesting(request)
def hapustesting(request): return Testing().hapusTesting(request)
def hapussemuatesting(request): return Testing().hapusSemuaTesting(request)

'''
method yang digunakan untuk data training
'''

def uploaddatatraining(request): return ModelTraining.index(request)
def hapusdatatraining(request): return ModelTraining.remove(request)
def pilihdatatraining(request): return ModelTraining.select(request)

'''
method yang diguankan untuk feature
'''

def pilihfeature(request):return Feature.select(request)
def hapusfeature(request): return Feature.remove(request)
def feature(request): return Feature.index(request)