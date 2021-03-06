# Generated by Django 3.0.8 on 2020-07-28 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('youtubedl', '0002_auto_20200728_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_id', models.CharField(max_length=200)),
                ('thumbnail', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('playlist_id', models.CharField(max_length=200)),
                ('thumbnail', models.CharField(max_length=200)),
                ('average_rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('date', models.DateField()),
                ('duration', models.IntegerField()),
                ('categories', models.ManyToManyField(blank=True, to='youtubedl.Category')),
                ('videos', models.ManyToManyField(blank=True, to='youtubedl.Video')),
            ],
        ),
    ]
