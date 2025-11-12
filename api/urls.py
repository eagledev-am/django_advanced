from django.urls import path
from api.views import (
    RatingsNPlusOneAPIView, RatingsSelectRelatedAPIView, RatingsPrefetchRelatedAPIView ,
    MovieDynamicFilterAPIView,
    MovieUpdateFExpressionAPIView,
    MovieOnlyFieldsAPIView,
    MovieDeferFieldsAPIView,
    MovieValuesAPIView,
    MovieValuesListAPIView,
)

urlpatterns = [
    path('api/ratings-nplusone/', RatingsNPlusOneAPIView.as_view(), name='api_ratings_nplusone'),
    path('api/ratings-selectrelated/', RatingsSelectRelatedAPIView.as_view(), name='api_ratings_selectrelated'),
    path('api/ratings-prefetchrelated/', RatingsPrefetchRelatedAPIView.as_view(), name='api_ratings_prefetchrelated'),
    path('api/movies/filter/', MovieDynamicFilterAPIView.as_view(), name='movie_filter'),
    path('api/movies/update-title/', MovieUpdateFExpressionAPIView.as_view(), name='movie_update_f'),
    path('api/movies/only-fields/', MovieOnlyFieldsAPIView.as_view(), name='movie_only_fields'),
    path('api/movies/defer-fields/', MovieDeferFieldsAPIView.as_view(), name='movie_defer_fields'),
    path('api/movies/values/', MovieValuesAPIView.as_view(), name='movie_values'),
    path('api/movies/values-list/', MovieValuesListAPIView.as_view(), name='movie_values_list'),
]
