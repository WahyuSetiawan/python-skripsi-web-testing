import os
from django.core.exceptions import ValidationError

def validate_file_extension_csv(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_file_extension_pkl(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pkl']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_file_extension_txt(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')