
from django.db import models

# Create your models here.
class Genres(models.Model):
    genres = models.CharField(max_length=20,null=True,blank=True)

class MyCollection(models.Model):
    collection_uuid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    

class MovieCollection(models.Model):
    uuid = models.CharField(max_length=40,primary_key=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank= True)
    genres = models.ManyToManyField(Genres)
    collection_uuid = models.ForeignKey(MyCollection,on_delete=models.CASCADE)


