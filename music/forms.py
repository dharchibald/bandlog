from django import forms

from .models import *

class ArtistForm(forms.ModelForm):
  class Meta:
    model = Artist
    fields = ['name', 'from_date', 'to_date', 
              'country', 'bio', 'img_path']

class BandForm(forms.ModelForm):
  class Meta:
    model = Artist
    fields = ['name', 'members', 'from_date',
              'to_date', 'country', 'bio',
              'img_path']
