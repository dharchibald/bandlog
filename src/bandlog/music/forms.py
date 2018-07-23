from django import forms
from .models import Artist


class ArtistForm(forms.ModelForm):
  class Meta:
    model = Artist
    fields = ('last_name', 'first_name', 'from_date',
              'to_date', 'related', 'discog',
              'country', 'bio', 'img_path',)

class BandForm(forms.ModelForm):
  class Meta:
    model = Artist
    fields = ('last_name', 'from_date', 'to_date',
              'related', 'members', 'discog',
              'country', 'bio', 'img_path',)

class AlbumForm(forms.ModelForm):
  class Meta:
    model = Album
    fields = ('title', 'credits', 'release_date',
              'release_type', 'desc', 'img_path',)

class SongForm(forms.ModelForm):
  class Meta:
    model = Song
    fields = ('title', 'album', 'disc_num',
              'track_num', 'sample', 'lyrics') 

class GenreForm(form.ModelForm):
  class Meta:
    model = Genre
    fields = ('title', 'desc',)

class TagForm(form.ModelForm):
  class Meta:
    model = Tag
    fields = ('title', 'desc',)

class DiscussionForm(form.Model.Form):
  class Meta:
    model = Discussion
    fields = ('topic',)
