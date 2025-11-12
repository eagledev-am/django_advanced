from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255 , db_index=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['id']),
        ]

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rating = models.FloatField()
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'Rating {self.rating} by User {self.user.id} for Movie {self.movie.title}'

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=255)
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'Tag "{self.tag}" by User {self.user.id} for Movie {self.movie.title}'

class Link(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='link')
    imdb_id = models.IntegerField(null=True, blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True)

