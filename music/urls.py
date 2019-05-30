from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('artist/new', views.artist_create, name='artist_create'),
  path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
  path('release/album/<int:album_id>/', views.album_detail, name='album_detail'),
  path('release/track/<int:song_id>/', views.song_detail, name='song_detail'),
  path('search', views.search, name='search'),
]
