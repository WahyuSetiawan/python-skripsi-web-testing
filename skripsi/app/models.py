"""
Definition of models.
"""

from django.db import models

# Create your models here.

class ModelTraining(models.Model):
    id = models.AutoField(primary_key=True)
    datatraining = models.FileField(upload_to = 'datatraining')

    class Meta:
      db_table = "modeltraining"

class Setting(models.Model):
    tag = models.CharField(max_length = 100, null = False, default = "1",primary_key=True)
    valuedata = models.CharField(max_length = 100,null = False, default = "1")

    class Meta:
        db_table = "settingtraining"


class TestingData(models.Model):
    id = models.AutoField(primary_key = True)
    datatesting = models.FileField()

    class Meta:
        db_table = "jsonfiletesting"

class FeatureList(models.Model):
    id = models.AutoField(primary_key=True)
    FeatureList = models.FileField(upload_to = "featurelist")

    class Meta:
        db_table = "featureList"

class Stopwords(models.Model):
    id = models.AutoField(primary_key = True)
    stopwords = models.FileField(upload_to = "stopwords")

    class Meta:
        db_table = "stopwords"