# Generated by Django 3.0.8 on 2020-07-28 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtubedl', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
