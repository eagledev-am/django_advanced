from rest_framework import serializers
from api.models import Rating, Movie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['title', 'genres']

class RatingSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        model = Rating
        fields = ['rating', 'movie']
