from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Content(models.Model):
    content = models.CharField(max_length=10000)
    title = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    writer_id = models.IntegerField()

    def __str__(self):
        return f"on {self.date} : {self.content}"


class ProfileImg(models.Model):
    image = models.ImageField(upload_to='images/', default='default-profile.jpg')
    user_id = models.IntegerField()

    def __str__(self):
        return User.objects.get(id = self.user_id).username

class Comment(models.Model):
    comment = models.CharField(max_length=10000)
    content_id = models.IntegerField()
    user_id = models.IntegerField()
    date = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return f"{User.objects.get(id = self.user_id).username}: {self.comment}"


class Followed(models.Model):
    my_id = models.IntegerField()
    followed_id = models.IntegerField()

    def __str__(self):
        return User.objects.get(id = self.my_id).username