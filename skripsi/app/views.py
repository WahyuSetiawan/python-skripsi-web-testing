"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from .forms import UploadFileForm, UploadFileTesting
from .models import SaveFileForm, setting, testingData

from .TextMiningTesting import *

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
            datatrain = setting.objects.filter(tag = "datatrain")[0]

            print("".join([dir_path,'/../media/', str(testingfilesave.datatesting)]))

            train = TrainingData(
                "".join([dir_path,'/../media/', str(testingfilesave.datatesting)]), 
                'data/feature_list/id-stopwords.txt',
                "".join([dir_path,'/../media/', str(datatrain.valuedata)])
                )
            train.run()
    else:
        testignidlesave = testingData()

    return render(request,'app/testing.html', locals()
)

def upload(request):
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
    datatrain = setting.objects.filter(tag = "datatrain")[0]

    return render(
        request,
        'app/upload.html',
        locals()
    )


def pilihdatatraining(request):
    
    if request.method == "GET" and 'datatrain' in request.GET:
        datatrain = setting.objects.filter(tag = "datatrain")[0]

        if datatrain == None:
            set = setting(tag = "datatrain", valuedata = request.GET['datatrain'])
            set.save()
        else:
            datatrain.valuedata = request.GET['datatrain']
            datatrain.save()

    gambars = SaveFileForm.objects.all()

    return render(request, 'app/upload.html', locals())