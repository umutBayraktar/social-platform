from django.db import models
from user.models import UserNormal
from tag.models import Tag
from django.urls import reverse
from django.http import HttpResponse
# Create your models here.

class Discussion(models.Model):
    author = models.ForeignKey(UserNormal, on_delete=models.CASCADE,related_name="discussions")
    image = models.ImageField(verbose_name="Resim", blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    text = models.TextField(verbose_name="Tartisma Metni")
    tags = models.ManyToManyField(Tag, blank=True,related_name="discussion")
    likes = models.ManyToManyField(UserNormal, blank=True, related_name="discussion_like_list")
    dislikes = models.ManyToManyField(UserNormal, blank=True, related_name="discussion_dislike_list")
    pageview = models.PositiveIntegerField(default=0)
    video_url =models.URLField(blank=True,null=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("discussion:list_discussions")

class DiscussionComment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="discussion_comments")
    author = models.ForeignKey(UserNormal, on_delete=models.CASCADE, related_name="discuss_comments")
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    likes = models.ManyToManyField(UserNormal, blank=True, related_name="disc_comment_like_list")
    dislikes = models.ManyToManyField(UserNormal, blank=True, related_name="disc_comment_dislike_list")



class DiscussionReply(models.Model):

    parent=models.ForeignKey(DiscussionComment,on_delete=models.CASCADE,related_name="replies")
    author =models.ForeignKey(UserNormal)
    created_date=models.DateTimeField(auto_now_add=True)
    content =models.TextField()
    likes = models.ManyToManyField(UserNormal, blank=True, related_name="disc_reply_like_list")
    dislikes = models.ManyToManyField(UserNormal, blank=True, related_name="disc_reply_dislike_list")