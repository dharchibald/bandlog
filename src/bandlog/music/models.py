from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
  from_date = models.DateField(blank=True)
  to_date = models.DateField(blank=True)
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
  comments = GenericRelation('Comment')

  def is_band(self):
    return self.is_band


# Link between band members and the band.
# Also tracks how long each member was a part of the band.
class Membership(models.Model):
  member = models.ForeignKey(
    Artist,
    on_delete=models.CASCADE,
    related_name='band_memberships',
  )
  band = models.ForeignKey(
    Outline,
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


# Template for user-generated descriptors of albums/songs
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

  def __str__(self):
    return self.title

  @property
  def calculate_rating(self):
    sum = ratings.objects.all().aggregate(Sum('rating'))
    count = ratings.objects.count()
    return (sum/count)


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
  comments = GenericRelation('UserPost')

  def __str__(self):
    return self.title


# Page dedicated to discussions between users
class Discussion(models.Model):
  topic = models.CharField(max_length=127)
  create_time = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  posts = GenericRelation('UserPost')


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
  albums = models.ManyToManyField(
    Album,
    through='UserAlbum',
    blank=True,
  )


# User listens to an album/song
class UserListen(models.Model):
  user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='albums_heard',
  )
  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    related_name='listeners',
  )
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
  listens = models.PositiveIntegerField(default=0)
  last_update = models.DateField()


# User rating for an album/song
class UserRating(models.Model):
  user = models.ForeignKey(
    UserProfile,
    on_delete=models.CASCADE,
    related_name='rated',
  )
  content_type = models.ForeignKey(
    ContentType,
    on_delete=models.CASCADE,
    related_name='ratings',
  )
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
  rating = models.PositiveIntegerField()
  last_update = models.DateField(auto_now=true)


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
  genre = models.OneToOneField(
    Genre,
    on_delete=models.CASCADE,
    related_name='votes',
  )
  positive = models.BooleanField(default=true)


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
  tag = models.OneToOneField(
    Tag,
    on_delete=models.CASCADE,
    related_name='votes',
  )
  positive = models.BooleanField()

# Template for a user's post or comment
class UserPost(models.Model):
  author = models.ForeignKey(
    UserProfile,
    on_delete=models.SET_NULL,
    null=True,
    related_name='posts',
  )
  post = models.TextField(max_length=4095),
  date = models.DateTimeField(default=timezone.now)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()

  def __str__(self):
    return self.post
