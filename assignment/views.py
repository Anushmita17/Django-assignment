
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt

from django.db.models import Count
from django.http import HttpResponse
import requests



from assignment.models import MyCollection,MovieCollection


def index(request):
    url = 'https://demo.credy.in/api/v1/maya/movies/'
    header ={"Username":"iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0",
             "Password":"Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
            }
    response = requests.get(url,headers=header)
    if response.status_code==200:
        return HttpResponse(response)
    else:
        return HttpResponse(response)


class RegisterView (APIView):

    def post(self, request):
        user = request.data.get('username')
        password = request.data.get('password')
        if user and password:
            token = jwt.encode({'username':user,
                                'password':password})

            content = {'access_token':token}
            return Response(content)
        raise Exception('Please enter valid username and password')


class MovieView(APIView):
    
    def get(self, request):
        url = 'https://demo.credy.in/api/v1/maya/movies/'
        header = {
            "Username":"iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0",
            "Password":"Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
            }
        movies_request = requests.get(url,headers=header)
        if movies_request.status_code==200:
            return HttpResponse(movies_request)
        else:
            return HttpResponse("No data")
        

class CollectionView(APIView):
    def post(self,request):
        title = request.query_params.get('title')
        description = request.query_params.get('description')
        movies = request.query_params.get('movies')

        mycollection_obj = MyCollection(title=title,description=description)
        mycollection_obj.save()
        
        for data in movies:
           titles = data.get('title')
           description = data.get('description')
           genres = data.get('genres')
           uuids = data.get('uuid')
           
           moviecollection_obj = MovieCollection(title=titles,description=description,
                                 genres=genres,uuid=uuids,
                                 collection_uuid=mycollection_obj.collection_uuid)
           moviecollection_obj.save()
        return HttpResponse({"collection_uuid":mycollection_obj.collection_uuid})
    

    def get(self,request):
        collection_datas = MyCollection.objects.all()
        mycollection_data = []
        for collection_data in collection_datas:
            dict_data = {"title":collection_data.title,
                         "uuid":collection_data.collection_uuid,
                         "description":collection_data.description}
        
            mycollection_data.append(dict_data)
        movie_collection = MovieCollection.objects.annotate(
                               number_genres = Count('genres')).order_by('-genres')[:3]
        return HttpResponse({
            'is_success':'True',
            'data':{
                'collections':mycollection_data,
                'favourite_genres':movie_collection
                }
            })


class CollectionUuidView(APIView):
    
    def put(self,request,url_uuid):
        title = request.query_params.get('title')
        description = request.query_params.get('description')
        movies = request.query_params.get('movies')

        updated_mycollection = MyCollection.objects.filter(collection_uuid=url_uuid).update(
                                                          title=title,description=description)
        
        updated_mycollection.save()
        
        for movies_data in movies:
            titles = movies_data.get('title')
            description = movies_data.get('description')
            genres = movies_data.get('genres')
            uuids = movies_data.get('uuid')
            update_moviecollections = MovieCollection.objects.filter(collection_uuid=url_uuid,uuid=uuids).first()
            update_moviecollections.update(title=titles,description=description,
                genres=genres)
            update_moviecollections.save()

    def get(self,request,url_uuid):
        collection_updated_datas = MyCollection.objects.filter(collection_uuid=url_uuid).first()

        movies_datas = MovieCollection.objects.filter(collection_uuid=url_uuid)
        movie_list=[]
        for movies_data in movies_datas:
            movie_list_data = {
                "title":movies_data.title,
                "description":movies_data.description,
                "genres":movies_data.genres,
                "uuid":movies_data.uuid
            }
            movie_list.append(movie_list_data)
        return HttpResponse(
            {
                "title":collection_updated_datas.title,
                "description":collection_updated_datas.description,
                "movies":movie_list
            }
        )

    def delete(self,request,url_uuid):
        collection_data = MyCollection.objects.filter(collection_uuid=url_uuid).first()

        movies_datas = MovieCollection.objects.filter(collection_uuid=url_uuid)
        for movie in movies_datas:
            movie.delete()
        movies_datas.save()
        collection_data.delete()
        collection_data.save()

