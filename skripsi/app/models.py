"""
Definition of models.
"""

from django.db import models

# Create your models here.

class SaveFileForm(models.Model):
    id = models.AutoField(primary_key=True)
    datatraining = models.FileField(upload_to = 'datatraining')

    class Meta:
      db_table = "SaveFileForm"

class setting(models.Model):
    tag = models.CharField(max_length = 100, null = False, default = "1",primary_key=True)
    valuedata = models.CharField(max_length = 100,null = False, default = "1")

    class Meta:
        db_table = "settingtraining"


class testingData(models.Model):
    datatesting = models.FileField()

    class Meta:
        db_table = "jsonfiletesting"

class FeatureList(models.Model):
    id = models.AutoField(primary_key=True)
    FeatureList = models.FileField(upload_to = "featurelist")

    class Meta:
        db_table = "featureList"