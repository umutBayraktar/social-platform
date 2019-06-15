from django.db import models
from django.urls import reverse


"""
class Follower(models.Model):
    owner     = models.ForeignKey(UserNormal)
    followers = models.ForeignKey(UserNormal)



class Following(models.Model):
    owner     = models.ForeignKey(UserNormal)
    following = models.ForeignKey(UserNormal)"""


class Tag(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("index")