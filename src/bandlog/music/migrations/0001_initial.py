# Generated by Django 2.0.6 on 2018-08-03 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('release_date', models.DateField(blank=True)),
                ('release_type', models.CharField(choices=[('SG', 'Single'), ('EP', 'Extended Play'), ('LP', 'Long Play')], default='LP', max_length=2)),
                ('desc', models.TextField(blank=True, max_length=2047)),
                ('img_path', models.URLField(blank=True, max_length=255)),
                ('avg_rating', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
            ],
            options={
                'ordering': ['release_date'],
                'get_latest_by': ['release_date'],
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(db_index=True, max_length=127)),
                ('first_name', models.CharField(blank=True, max_length=31)),
                ('is_band', models.BooleanField()),
                ('from_date', models.DateField(blank=True)),
                ('to_date', models.DateField(blank=True)),
                ('avg_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('country', models.CharField(blank=True, max_length=31)),
                ('bio', models.TextField(blank=True, max_length=2047)),
                ('img_path', models.URLField(blank=True, max_length=255)),
                ('discog', models.ManyToManyField(blank=True, related_name='artists', to='music.Album')),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=127)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=31)),
                ('desc', models.TextField(blank=True, max_length=2047)),
                ('subgenres', models.ManyToManyField(blank=True, related_name='supergenres', to='music.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='GenreVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('positive', models.BooleanField(default=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre_votes', to='contenttypes.ContentType')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='music.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(blank=True)),
                ('to_date', models.DateField(blank=True)),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_memberships', to='music.Artist')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='band_memberships', to='music.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('disc_num', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('track_num', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sample', models.URLField(blank=True, max_length=255)),
                ('lyrics', models.TextField(blank=True, max_length=8191)),
                ('avg_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tracks', to='music.Album')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=31)),
                ('desc', models.TextField(blank=True, max_length=2047)),
            ],
        ),
        migrations.CreateModel(
            name='TagVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('positive', models.BooleanField(default=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_votes', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='music.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='UserListen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('listens', models.PositiveIntegerField(default=0)),
                ('last_update', models.DateField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listeners', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('favorites', models.ManyToManyField(blank=True, to='music.Artist')),
                ('friends', models.ManyToManyField(blank=True, related_name='_userprofile_friends_+', to='music.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('rating', models.PositiveIntegerField()),
                ('last_update', models.DateField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='music.UserProfile')),
            ],
            options={
                'get_latest_by': 'last_update',
            },
        ),
        migrations.AddField(
            model_name='userpost',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='music.UserProfile'),
        ),
        migrations.AddField(
            model_name='userpost',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='userlisten',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listens', to='music.UserProfile'),
        ),
        migrations.AddField(
            model_name='tagvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_votes', to='music.UserProfile'),
        ),
        migrations.AddField(
            model_name='genrevote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genre_votes', to='music.UserProfile'),
        ),
        migrations.AddField(
            model_name='artist',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='bands', through='music.Membership', to='music.Artist'),
        ),
        migrations.AddField(
            model_name='artist',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='_artist_related_+', to='music.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='credits',
            field=models.ManyToManyField(blank=True, related_name='credited_on', to='music.Artist'),
        ),
        migrations.AlterUniqueTogether(
            name='userrating',
            unique_together={('user', 'content_type', 'object_id')},
        ),
        migrations.AlterUniqueTogether(
            name='tagvote',
            unique_together={('user', 'content_type', 'object_id', 'tag')},
        ),
        migrations.AlterIndexTogether(
            name='tagvote',
            index_together={('content_type', 'object_id')},
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together={('album', 'disc_num', 'track_num')},
        ),
        migrations.AlterUniqueTogether(
            name='genrevote',
            unique_together={('user', 'content_type', 'object_id', 'genre')},
        ),
        migrations.AlterIndexTogether(
            name='genrevote',
            index_together={('content_type', 'object_id')},
        ),
    ]
