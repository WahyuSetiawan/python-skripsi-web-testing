"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.forms import UploadFileForm, UploadFileTesting, UploadFileFeature
from app.models import ModelTraining, Setting, TestingData, FeatureList

from app.Utility.TextMiningTesting import *

from app.Controller.FeatureList import FeatureController
from app.Controller.ModelTraining import ModelTrainingController
from app.Controller.Testing import TestingController
from app.Controller.Stopwords import StopwordsController

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

def testing(request): return TestingController().index(request)
def daftartesting(request): return TestingController().daftarTesting(request)
def hapustesting(request): return TestingController().hapusTesting(request)
def hapussemuatesting(request): return TestingController().hapusSemuaTesting(request)

'''
method yang digunakan untuk data training
'''

def uploaddatatraining(request): return ModelTrainingController().index(request)
def hapusdatatraining(request): return ModelTrainingController().remove(request)
def pilihdatatraining(request): return ModelTrainingController().select(request)

'''
method yang diguankan untuk feature
'''

def pilihfeature(request):return FeatureController().select(request)
def hapusfeature(request): return FeatureController().remove(request)
def feature(request): return FeatureController().index(request)

'''
method yang digunakan untuk stopwords
'''

def pilihstopwords(request):return StopwordsController().select(request)
def hapusstopwords(request): return StopwordsController().remove(request)
def uploadstopwords(request): return StopwordsController().index(request)
