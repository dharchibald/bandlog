from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Template for individual artists - represents an artist by name.
# If an artist is further defined, then the details will be stored
# in the artist's Outline.
class Artist(models.Model):
  name = models.CharField(max_length=127, db_index=True)
  outline = models.OneToOneField(
    'Outline',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='base',
  )

  def __str__(self):
    return name

  def get_profile(self):
    return outline


# Template for bands/individuals that hold more info than a name.
class Outline(models.Model):
  is_band = models.BooleanField()
  members = models.ManyToManyField(
    Artist,
    through='Membership',
    blank=True,
    related_name='bands',
  )
  related = models.ManyToManyField('self', blank=True)
  from_date = models.DateField(null=True, blank=True)
  to_date = models.DateField(null=True, blank=True)
  discog = models.ManyToManyField('Album', blank=True)
  avg_rating = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    null=True,
    blank=True,
  )
  country = models.CharField(max_length=31, blank=True)
  bio = models.TextField(max_length=2047, blank=True)
  img_path = models.URLField(max_length=255, blank=True)

  def is_band(self):
    return self.is_band


# Link between band members and the band.
# Also tracks how long each member was a part of the band.
class Membership(models.Model):
  member = models.ForeignKey(
    Artist,
    on_delete=models.SET_NULL,
    null=True,
    related_name='band_memberships',
  )
  band = models.ForeignKey(
    Outline,
    on_delete=models.SET_NULL,
    null=True,
    related_name='member_memberships',
  )
  from_date = models.DateField(null=True, blank=True)
  to_date = models.DateField(null=True, blank=True)


# Template for genres an album may belong to.
class Genre(models.Model):
  title = models.CharField(max_length=31)
  desc = models.TextField(max_length=2047, blank=True)
  subgenres = models.ManyToManyField(
    'Genre',
    symmetrical=False,
    null=True,
    blank=True,
    related_name='supergenres',
  )


class Tag(models.Model):
  title = models.CharField(max_length=31)
  desc = models.TextField(max_length=2047, blank=True)


# Template for an album release from an artist.
class Album(models.Model):
  SINGLE = 'SG'
  EP = 'EP'
  LP = 'LP'
  TYPE_CHOICES = (
    (SINGLE, 'Single'),
    (EP, 'Extended Play'),
    (LP, 'Long Play'),
  )

  title = models.CharField(max_length=127)
  credits = models.ManyToManyField(
    Artist,
    blank=True,
    related_name='credited_on',
  )
  genres = models.ManyToManyField(
    Genres,
    blank=True,
    related_name='albums',
  )
  release_date = models.DateField(blank=True)
  release_type = models.CharField(
    max_length=2,
    choices=TYPE_CHOICES,
    default=LP,
  )
  desc = models.TextField(max_length=2047, blank=True)
  img_path = models.URLField(max_length=255, blank=True)
  avg_rating = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    null=True,
  )

  def __str__(self):
    return self.title

  def get_type(self):
    return self.release_type


# Template for the songs that make up releases.
class Song(models.Model):
  title = models.CharField(max_length=127)
  album = models.ForeignKey(
    Album,
    on_delete=models.SET_NULL,
    null=True,
    related_name='tracks',
  )
  disc_num = models.PositiveSmallIntegerField(null=True, blank=True)
  track_num = models.PositiveSmallIntegerField(null=True, blank=True)
  avg_rating = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    null=True,
  )
  sample = models.URLField(max_length=255, blank=True)
  lyrics = models.TextField(max_length=8191, blank=True)

  def __str__(self):
    return self.title


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  friends = models.ManyToManyField(
    'self',
    symmetrical=True,
    blank=True,
  )
  bio = models.TextField(blank=True)
  favorites = models.ManyToManyField(Artist, blank=True)
  albums = models.ManyToManyField(
    Album,
    through='UserAlbum',
    blank=True,
  )

# Relationship between a user and an album
class UserAlbum(models.Model):
  user = models.ForeignKey(
    UserProfile,
    on_delete=models.SET_NULL,
    null=True,
  )
  album = models.ForeignKey(
    Album,
    on_delete=models.SET_NULL,
    null=True,
  )
  listens = PositiveIntegerField(default=0)
  last_listen = DateField(blank=True)
  rating = PositiveIntegerField(null=True, blank=True)


# Relationship between a user and a song
  user = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
  )
  song = models.ForeignKey(
    Song,
    on_delete=models.SET_NULL,
    null=True,
  )
  listens = PositiveIntegerField(default=0)
  last_listen = DateField(blank=true)
  rating = PositiveSmallIntegerField(null=True, blank=true)


# Template for a user's post or comment
class UserPost(models.Model):
  user = models.ForeignKey(
    UserProfile,
    on_delete=models.SET_NULL,
    null=True,
    related_name='posts',
  )
  post = models.TextField(),
  date = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.post
