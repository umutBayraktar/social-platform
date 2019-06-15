from django.db import models
from django.contrib.auth.models import User
from tag.models import Tag
from django_countries.fields import CountryField
# Create your models here.

class UserStatistics(models.Model):
    article_count = models.PositiveIntegerField(default=0)
    discussion_count =models.PositiveIntegerField(default=0)
    comment_count =models.PositiveIntegerField(default=0)
    follower_count=models.PositiveIntegerField(default=0)



class UserNormal(User):
    birthday=models.DateTimeField(verbose_name="Doğum Günü",blank=True,null=True)
    gender=models.BinaryField(verbose_name="Cinsiyet")
    about=models.TextField(verbose_name="Hakkımda",blank=True,null=True)
    photo=models.ImageField(blank=True,null=True,verbose_name="Profil Fotoğrafı")
    country=CountryField(blank_label="Ülke Seçiniz",blank=True,multiple=True)
    language_choice=models.CharField(max_length=5,default="TR")
    statistics=models.OneToOneField(UserStatistics,blank=True,null=True)
    followers=models.ManyToManyField("self",blank=True,null=True)
    following=models.ManyToManyField("self",blank=True,null=True)
    tags = models.ManyToManyField(Tag, related_name="user", blank=True, null=True)

