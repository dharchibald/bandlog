from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Artist

# Create your views here.

def index(request):
  return render(request, 'music/index.html', {})

def artist(request, artist_id):
  return HttpResponse("You're looking at artist %s." % artist_id)
