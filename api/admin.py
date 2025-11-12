from django.contrib import admin
from .models import Genre, Movie, Rating, Tag, Link

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Tag)
admin.site.register(Link)
