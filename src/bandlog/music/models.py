from django.db import models

# Create your models here.

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


class Outline(models.Model):
  is_band = models.BooleanField()
  members = models.ManyToManyField(
    Artist,
    through='Membership',
    symmetrical=False,
    related_name='bands',
  )
  related = models.ManyToManyField('self')
  from_date = models.DateField(
    auto_now=False,
    auto_now_add=False,
    null=True,
    blank=True,
  )
  to_date = models.DateField(
    auto_now=False,
    auto_now_add=False,
    null=True,
    blank=True,
  )
  discog = models.ManyToManyField('Album')
  avg_rating = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    null=True,
  )
  country = models.CharField(max_length=31, blank=True)
  bio = models.TextField(max_length=2047, blank=True)
  img_path = models.URLField(max_length=255, blank=True)

  def is_band(self):
    return self.is_band


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
  from_date = models.DateField(
    auto_now=False,
    auto_now_add=False,
    null=True,
    blank=True,
  )
  to_date = models.DateField(
    auto_now=False,
    auto_now_add=False,
    null=True,
    blank=True,
  )


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
  release_date = models.DateField(
    auto_now=False, 
    auto_now_add=False,
    blank=True,
  )
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
  details = models.OneToOneField(
    'SongExtend',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='base',
  )

  def __str__(self):
    return self.title


class SongExtend(models.Model):
  sample = models.URLField(max_length=255, blank=True)
  lyrics = models.TextField(max_length=8191, blank=True)
