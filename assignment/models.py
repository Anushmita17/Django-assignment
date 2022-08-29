import uuid


import uuid

from django.db import models


class Genres(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    genres = models.CharField(max_length=20,null=True,blank=True)


class MyCollection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    

class MovieCollection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank= True)
    genres = models.ManyToManyField(Genres,null=True,blank= True)
    collection = models.ForeignKey(MyCollection,null=True,blank= True,on_delete=models.CASCADE)


