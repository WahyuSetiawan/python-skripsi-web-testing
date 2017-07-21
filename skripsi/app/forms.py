"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.Utility.formatChecker import validate_file_extension_csv, validate_file_extension_pkl, validate_file_extension_txt

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class UploadFileForm(forms.Form):
    datatraining = forms.FileField(validators=[validate_file_extension_pkl])

class UploadFileTesting(forms.Form):
    datatesting = forms.FileField(validators=[validate_file_extension_csv])

class UploadFileFeature(forms.Form):
    featurefile = forms.FileField(validators=[validate_file_extension_txt])

class StopwordsFrom(forms.Form):
    stopword = forms.FileField(validators=[validate_file_extension_txt])