from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Artist

# Create your views here.

def index(request):
  return render(request, 'music/index.html', {})

def artist_detail(request, artist_id):
  artist = get_object_or_404(Artist, pk=artist_id)

  if artist.is_band:
    return render(request, 'music/band.html', {'artist': artist})
  else:
    return render(request, 'music/artist.html', {'artist': artist})
