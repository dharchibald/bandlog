from django import forms

class ArtistForm(forms.ModelForm):
  class Meta:
    model = Artist
    fields = ['first_name', 'last_name', 'from_date',
              'to_date', 'country', 'bio',
              'img_path']

class BandForm(forms.ModelForm):
  class Meta:
    model = Artist
    fields = ['last_name', 'members', 'from_date',
              'to_date', 'country', 'bio',
              'img_path']
