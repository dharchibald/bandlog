import random

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .library import group

from .models import Artist
from .models import Membership
from .models import Genre
from .models import Tag
from .models import Album
from .models import Song


# Create your views here.

def index(request):

  # Get featured artists
  # Randomly selected artists with average score of 3 or above
  base_score = 3
  artists = Artist.objects.filter(avg_rating__gte=base_score)
  ids = artists.values_list('id', flat=True)
  ids = list(ids)
  n = 4
  if artists.count() < n:
    rand_ids = random.sample(ids, artists.count())
  else:
    rand_ids = random.sample(ids, n)
  featured = Artist.objects.filter(id__in=rand_ids)
  featured_num = featured.count()

  # Get latest releases (latest first)
  card_num = 4
  latest = Album.objects.all().order_by('-release_date')
  latest_chunks = list(group(latest, card_num))

  return render(request, 'music/index.html', {'featured': featured,
                                              'featured_num': featured_num,
                                              'latest': latest_chunks})


def artist_detail(request, artist_id):

  # Get specified artist by artist_id and separate releases
  artist = get_object_or_404(Artist, pk=artist_id)
  releases = artist.discog.order_by('release_date')
  long_plays = releases.filter(release_type__exact='LP')
  extend_plays = releases.filter(release_type__exact='EP')
  singles = releases.filter(release_type__exact='SG')

  # Similar artists - join top 2 genres and top 5 tags and increment an entry's
  # "score" when found in a shared genre or tag
  # Sort output by score

  if artist.is_band:
    return render(request, 'music/band.html', {'artist': artist})
  else:
    return render(request, 'music/artist.html', {'artist': artist})


def album_detail(request, album_id):
  album = get_object_or_404(Album, pk=album_id)

  return render(request, 'music/album.html', {'album': album,})


def song_detail(request, song_id):
  song = get_object_or_404(Song, pk=song_id)

  return render(request, 'music/song.html', {'song': song})
