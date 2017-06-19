"""
Definition of urls for skripsi.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),

    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    url(r'^testing',  app.views.testing, name="testing"),
    url(r'^daftartesting',  app.views.daftartesting, name="daftartesting"),
    url(r'^hapustesting',  app.views.hapustesting, name="hapustesting"),
    url(r'^hapussemuatesting',  app.views.hapussemuatesting, name="hapussemuatesting"),


    url(r'^uploaddatatraining',  app.views.uploaddatatraining, name="uploaddatatraining"),
    url(r'^pilihdatatraining',  app.views.pilihdatatraining, name="pilihdatatraining"),
    url(r'^hapusdatatraining',  app.views.hapusdatatraining, name="hapusdatatraining"),

    url(r'^feature',  app.views.feature, name="feature"),
    url(r'^pilihfeature',  app.views.pilihfeature, name="pilihfeature"),
    url(r'^hapusfeature',  app.views.hapusfeature, name="hapusfeature"),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]

