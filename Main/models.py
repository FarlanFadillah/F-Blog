from django.db import models
from datetime import datetime

# Create your models here.

class Content(models.Model):
    content = models.CharField(max_length=10000)
    title = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    writer_id = models.IntegerField()


class ProfileImg(models.Model):
    image = models.ImageField(upload_to='images/', default='default-profile.jpg')
    user_id = models.IntegerField()

class Comment(models.Model):
    comment = models.CharField(max_length=10000)
    content_id = models.IntegerField()
    user_id = models.IntegerField()
    date = models.DateTimeField(default=datetime.now(), blank=True)


class Followed(models.Model):
    my_id = models.IntegerField()
    followed_id = models.IntegerField()