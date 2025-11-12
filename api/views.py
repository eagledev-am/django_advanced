from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Rating
from api.serializers import MovieSerializer, RatingSerializer
from django.db.models import Q, F
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Movie, Rating

class RatingsNPlusOneAPIView(APIView):

    def get(self, request):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response({
            'note': 'N+1 query problem - no select_related/prefetch_related',
            'ratings': serializer.data,
        })

class RatingsSelectRelatedAPIView(APIView):
    def get(self, request):
        ratings = Rating.objects.select_related('movie').all()
        serializer = RatingSerializer(ratings, many=True)
        return Response({
            'note': 'Optimized with select_related (single query for ratings+movies)',
            'ratings': serializer.data,
        })

class RatingsPrefetchRelatedAPIView(APIView):
    def get(self, request):
        ratings = Rating.objects.select_related('movie').prefetch_related('movie__genres').all()
        serializer = RatingSerializer(ratings, many=True)
        return Response({
            'note': 'Optimized with select_related and prefetch_related for many-to-many genres',
            'ratings': serializer.data,
        })


# Dynamic filter with Q()

class MovieDynamicFilterAPIView(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword')
        genre_name = request.query_params.get('genre')
        query = Q()
        if keyword:
            query &= Q(title__icontains=keyword)
        if genre_name:
            query &= Q(genres__name__iexact=genre_name)
        movies = Movie.objects.filter(query).distinct()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


#  Update fields using F()

class MovieUpdateFExpressionAPIView(APIView):
    def put(self, request):
        movie_id = request.data.get('id')
        append_text = request.data.get('append', ' updated')
        updated = Movie.objects.filter(id=movie_id).update(
            title=F('title') + append_text
        )
        return Response({'updated_count': updated})


# Select specific fields using only()

class MovieOnlyFieldsAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.only('id', 'title')[:10]
        response = [{'id': m.id, 'title': m.title} for m in movies]
        return Response(response)


# Select fields using defer()

class MovieDeferFieldsAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.defer('genres')[:10]
        response = [{'id': m.id, 'title': m.title} for m in movies]
        return Response(response)


# Retrieve data as dict using values()

class MovieValuesAPIView(APIView):
    def get(self, request):
        movies_dict = list(Movie.objects.values('id', 'title')[:10])
        return Response(movies_dict)


# Retrieve data as tuple using values_list()

class MovieValuesListAPIView(APIView):
    def get(self, request):
        movies_tuples = list(Movie.objects.values_list('id', 'title')[:10])
        return Response(movies_tuples)
