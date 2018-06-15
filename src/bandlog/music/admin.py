from django.contrib import admin

# Register your models here.

from .models import Artist, Membership, Album, Song, Genre, Tag
from .models import UserProfile, UserRating, GenreVote, TagVote, Discussion, UserPost

admin.site.register(Artist)
admin.site.register(Membership)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(UserRating)
admin.site.register(GenreVote)
admin.site.register(TagVote)
admin.site.register(Discussion)
admin.site.register(UserPost)

