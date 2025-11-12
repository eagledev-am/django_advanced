import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import User, Genre, Movie, Rating, Tag, Link

class Command(BaseCommand):
    help = 'Load MovieLens dataset using single admin user for all entries'

    @transaction.atomic
    def load_movies(self):
        with open('data/movies.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                movie_id = int(row['movieId'])
                title = row['title']
                genres_raw = row['genres']
                movie, created = Movie.objects.get_or_create(id=movie_id, defaults={'title': title})
                if created:
                    genres = genres_raw.split('|') if genres_raw else []
                    genre_objs = []
                    for g in genres:
                        genre, _ = Genre.objects.get_or_create(name=g)
                        genre_objs.append(genre)
                    movie.genres.set(genre_objs)

    @transaction.atomic
    def load_users_ratings_tags_links(self):
        # Get or create single admin user
        admin_user, _ = User.objects.get_or_create(id=1, username='admin', defaults={'password': 'pbkdf2_sha256$dummy'})

        # Load ratings
        with open('data/ratings.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    movie_id = int(row['movieId'])
                    rating_val = float(row['rating'])
                    timestamp_val = int(row['timestamp'])
                except ValueError:
                    continue

                try:
                    movie = Movie.objects.get(id=movie_id)
                except Movie.DoesNotExist:
                    continue

                Rating.objects.get_or_create(
                    user=admin_user,
                    movie=movie,
                    rating=rating_val,
                    timestamp=timestamp_val
                )

        # Load tags
        with open('data/tags.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    movie_id = int(row['movieId'])
                    tag_text = row['tag']
                    timestamp_val = int(row['timestamp'])
                except ValueError:
                    continue

                try:
                    movie = Movie.objects.get(id=movie_id)
                except Movie.DoesNotExist:
                    continue

                Tag.objects.get_or_create(
                    user=admin_user,
                    movie=movie,
                    tag=tag_text,
                    timestamp=timestamp_val
                )

        # Load links
        with open('data/links.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    movie_id = int(row['movieId'])
                    imdb_id = int(row['imdbId']) if row['imdbId'] else None
                    tmdb_id = int(row['tmdbId']) if row['tmdbId'] else None
                except ValueError:
                    continue

                try:
                    movie = Movie.objects.get(id=movie_id)
                except Movie.DoesNotExist:
                    continue

                Link.objects.get_or_create(
                    movie=movie,
                    imdb_id=imdb_id,
                    tmdb_id=tmdb_id
                )

    def handle(self, *args, **kwargs):
        self.stdout.write("Loading movies...")
        self.load_movies()

        self.stdout.write("Loading ratings, tags, and links with admin user...")
        self.load_users_ratings_tags_links()

        self.stdout.write(self.style.SUCCESS("Data loaded successfully using single admin user."))
