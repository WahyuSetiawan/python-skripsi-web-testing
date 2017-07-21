"""
Definition of models.
"""

from django.db import models
from app.Utility.formatChecker import validate_file_extension_csv, validate_file_extension_txt, validate_file_extension_pkl
# Create your models here.

class ModelTraining(models.Model):
    id = models.AutoField(primary_key=True)
    datatraining = models.FileField(upload_to = 'datatraining', validators=[validate_file_extension_pkl])

    class Meta:
      db_table = "modeltraining"

class Setting(models.Model):
    tag = models.CharField(max_length = 100, null = False, default = "1",primary_key=True)
    valuedata = models.CharField(max_length = 100,null = False, default = "1")

    class Meta:
        db_table = "settingtraining"


class TestingData(models.Model):
    id = models.AutoField(primary_key = True)
    datatesting = models.FileField(validators=[validate_file_extension_csv])

    class Meta:
        db_table = "jsonfiletesting"

class FeatureList(models.Model):
    id = models.AutoField(primary_key=True)
    FeatureList = models.FileField(upload_to = "featurelist",validators=[validate_file_extension_txt])

    class Meta:
        db_table = "featureList"

class Stopwords(models.Model):
    id = models.AutoField(primary_key = True)
    stopwords = models.FileField(upload_to = "stopwords", validators=[validate_file_extension_txt])

    class Meta:
        db_table = "stopwords"