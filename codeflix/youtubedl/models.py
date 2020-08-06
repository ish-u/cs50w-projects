from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60)
    def __str__(self):
        return f"{self.pk} -  {self.name}"

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_id = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    date = models.DateField()
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.pk} -  {self.title}"

class Playlist(models.Model):
    name = models.CharField(max_length=60)
    playlist_id = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    videos = models.ManyToManyField(Video,blank=True)
    categories = models.ManyToManyField(Category,blank=True)
    average_rating = models.DecimalField(max_digits=3,decimal_places=2,null=True)
    date = models.DateField()
    duration = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.pk} - {self.name}"
