from lib2to3.pgen2 import token
from django.urls import path 
from . import views

urlpatterns = [
    path('assignment/',views.index, name = 'index'),
    path('register/',views.RegisterView.as_view(), name ='register'),
    path('movies/',views.MovieView.as_view(),name= 'movies'),
    path('collection/',views.CollectionView.as_view(),name='collection'),
    path(r'^collection/(?P<url_uuid>[0-9A-Za-z]+)$',views.CollectionUuidView.as_view(),name='collectionuuid')
    
]