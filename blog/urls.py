from django.urls import URLPattern, path

from . import views

app_name = 'movie'


urlpatterns = [
    path('',views.IndexHome.as_view(),name='home'),

    path('<int:year>/<int:month>/<int:day>/<slug:movie>/kinolife',views.detail_movie,name='detail_cinema'),

    path('<int:movie_id>/share/',views.share_movie,name='share_cinema'),

    path('<int:movie_id>/comment/',views.movie_comment,name='commentd')
]