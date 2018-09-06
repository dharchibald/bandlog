import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q

from .library import group, pagebreak
from .models import *
from .forms import *


# Create your views here.

def index(request):

  # Get featured artists
  # Randomly selected artists with average score of 3 or above
  template = 'music/index.html'
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

  context = {
    'featured': featured,
    'featured_num': featured_num,
    'latest': latest_chunks}

  return render(request, template, context)


def artist_detail(request, artist_id):

  artist = get_object_or_404(Artist, pk=artist_id)

  if artist.is_band:
    template = 'music/band.html'
  else:
    template = 'music/artist.html'

  releases = artist.discog.order_by('release_date')
  long_plays = releases.filter(release_type__exact='LP')
  extend_plays = releases.filter(release_type__exact='EP')
  singles = releases.filter(release_type__exact='SG')

  # Similar artists - join top 2 genres and top 5 tags and increment an entry's
  # "score" when found in a shared genre or tag
  # Sort output by score

  context = {'artist': artist,
             'long_plays': long_plays,
             'extend_plays': extend_plays,
             'singles': singles}

  return render(request, template, context)

# Allows users to create artists in the database
def artist_create(request):

  template = 'music/artist_edit.html'

  if request.method == 'POST':
    form = ArtistForm(request.POST)

    if form.is_valid():
      new_artist = form.save(commit=False)
      new_artist.is_band = False
      new_artist.save()
      form.save_m2m()
      return redirect('artist_detail', pk=new_artist.pk)

  else:
    form = ArtistForm()

  context = {'form': form}

  return render(request, template, context)


def band_create(request):

  template = 'music/artist_edit.html'

  if request.method == 'POST':

    form = BandForm(request.POST)

    if form.is_valid():
      new_band = form.save(commit=False)
      new_band.is_band = True
      new_band.save()
      form.save_m2m()
      return redirect('music/artist_detail', pk=new_band.pk)

    else:
      form = ArtistForm()

  context = {'form': form}

  return render(request, template, context)


def artist_edit(request, pk):

  template = 'music/artist_edit.html'
  artist = get_object_or_404(Artist, pk=pk)

  if request.method == "POST":

    form = ArtistForm(request.POST, instance=post)

    if form.is_valid():
      artist = form.save(commit=False)
      artist.save()
      form.save_m2m()
      return HttpResponseRedirect(reverse('artist_success', args=[str(artist.id)]))

    else:
      form = ArtistForm(instance=post)

  context = {'form': form}

  return render(request, template, context)


def album_detail(request, album_id):

  template = 'music/album.html'
  album = get_object_or_404(Album, pk=album_id)
  context = {'album': album}

  return render(request, template, context)


def song_detail(request, song_id):

  template = 'music/song.html'
  song = get_object_or_404(Song, pk=song_id)
  context = {'song': song}

  return render(request, template, context)


def search(request):

  template = 'music/search.html'
  query = request.GET.get('q')
  # Break query up into substrings?

  artists = Artist.objects.filter(Q(name__icontains=query))
  #albums = Albums.objects.filter(Q(title__icontains=query))
  #songs = Albums.objects.filter(Q(title__icontains=query))
  #object_list = list(chain(artists, albums, songs))

  #pages = pagebreak(request, object_list, 10)

  pages = pagebreak(request, artists, 10)

  context = {'items': pages[0],
             'page_range': pages[1],
             'query': query}

  return render(request, template, context)
