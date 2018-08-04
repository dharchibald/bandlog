from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.

# Template for a music artist.
class Artist(models.Model):
  last_name = models.CharField(max_length=127, db_index=True)
  first_name = models.CharField(max_length=31, blank=True)
  is_band = models.BooleanField()
  members = models.ManyToManyField(
    'self',
    through='Membership',
    symmetrical=False,
    blank=True,
    related_name='bands',
  )
  related = models.ManyToManyField(
    'self', 
    blank=True
  )
  from_date = models.DateField(blank=True)
  to_date = models.DateField(blank=True)
  discog = models.ManyToManyField(
    'Album',
    blank=True,
    related_name='artists',
  )
  avg_rating = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    null=True,
    blank=True,
  )
  country = models.CharField(max_length=31, blank=True)
  bio = models.TextField(max_length=2047, blank=True)
  img_path = models.URLField(max_length=255, blank=True)
  comments = GenericRelation('UserPost')

  def __str__(self):
    if self.is_band:
      return self.last_name
    else:
      return '{0}, {1}'.format(self.last_name, self.first_name)

  def get_absolute_url(self):
    return reverse('artist_detail', args=[str(self.id)])


# Link between band members and the band.
# Tracks how long each member was a part of the band.
class Membership(models.Model):
  member = models.ForeignKey(
    Artist,
    on_delete=models.CASCADE,
    related_name='band_memberships',
  )
  band = models.ForeignKey(
    Artist,
    on_delete=models.CASCADE,
    related_name='member_memberships',
  )
  from_date = models.DateField(blank=True)
  to_date = models.DateField(blank=True)


# Template for genres an album may belong to.
class Genre(models.Model):
  title = models.CharField(max_length=31)
  desc = models.TextField(max_length=2047, blank=True)
  subgenres = models.ManyToManyField(
    'Genre',
    symmetrical=False,
    blank=True,
    related_name='supergenres',
  )

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('genre_detail', args=[str(self.id)])


# Template for user-generated descriptors of albums/songs
class Tag(models.Model):
  title = models.CharField(max_length=31)
  desc = models.TextField(max_length=2047, blank=True)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('tag_detail', args=[str(self.id)])


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
  ratings = GenericRelation('UserRating')
  comments = GenericRelation('UserPost')

  class Meta:
    get_latest_by = ['release_date']
    ordering = ['release_date']

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('album_detail', args=[str(self.id)])

  @property
  def calculate_rating(self):
    return UserRating.objects.filter(content_object=self).aggregate(Avg('rating'))

  def update_rating(self):
    self.avg_rating = self.calculate_rating()
    self.save()


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
  sample = models.URLField(max_length=255, blank=True)
  lyrics = models.TextField(max_length=8191, blank=True)
  avg_rating = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    null=True,
    blank=True,
  )
  ratings = GenericRelation('UserRating')
  comments = GenericRelation('UserPost')

  class Meta:
    unique_together = ('album', 'disc_num', 'track_num',)
    ordering = ['album', 'disc_num', 'track_num']

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('song_detail', args=[str(self.id)])

  def calculate_rating(self):
    return UserRating.objects.filter(content_object=self).aggregate(Avg('rating'))

  def update_rating(self):
    self.avg_rating = self.calculate_rating()
    self.save()


# Page dedicated to discussions between users
class Discussion(models.Model):
  topic = models.CharField(max_length=127)
  date = models.DateTimeField(auto_now_add=True)
  posts = GenericRelation('UserPost')

  def __str__(self):
    return date + " " + topic

  def get_absolute_urL(self):
    return reverse('discussion-detail', args=[str(self.id)])

  @property
  def last_update(self):
    return posts.latest().date


# Profile template for individual users
class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  friends = models.ManyToManyField(
    'self',
    symmetrical=True,
    blank=True,
  )
  bio = models.TextField(blank=True)
  favorites = models.ManyToManyField(Artist, blank=True)


# User listens to an album/song
class UserListen(models.Model):
  user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='listens',
  )
  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    related_name='listeners',
  )
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
  listens = models.PositiveIntegerField(default=0)
  last_update = models.DateField(auto_now=True)


# User rating for an album/song
class UserRating(models.Model):
  user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='ratings',
  )
  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    related_name='ratings',
  )
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
  rating = models.PositiveIntegerField()
  last_update = models.DateField(auto_now=True)

  class Meta:
    unique_together = (('user', 'content_type', 'object_id'),)
    get_latest_by = 'last_update'

  def save(self, *args, **kwargs):
    self.last_update = now()
    super(UserRating, self).save(*args, **kwargs)


# User votes for a genre applied to an album/song
class GenreVote(models.Model):
  user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='genre_votes',
  )
  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    related_name='genre_votes',
  )
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
  genre = models.ForeignKey(
    Genre,
    on_delete=models.CASCADE,
    related_name='votes',
  )
  positive = models.BooleanField(default=True)

  class Meta:
    unique_together = (('user', 'content_type', 'object_id', 'genre'),)
    index_together = (('content_type', 'object_id'),)


# User votes for individual tags on an album/song
class TagVote(models.Model):
  user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='tag_votes',
  )
  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    related_name='tag_votes',
  )
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
  tag = models.ForeignKey(
    Tag,
    on_delete=models.CASCADE,
    related_name='votes',
  )
  positive = models.BooleanField(default=True)

  class Meta:
    unique_together = (('user', 'content_type', 'object_id', 'tag'),)
    index_together = (('content_type', 'object_id'),)


# Template for a user's post or comment
class UserPost(models.Model):
  author = models.ForeignKey(
    UserProfile,
    on_delete=models.SET_NULL,
    null=True,
    related_name='posts',
  )
  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    related_name='posts',
  )
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
  body = models.TextField(max_length=4095),
  date = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.post
