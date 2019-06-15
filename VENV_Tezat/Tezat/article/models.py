from django.db import models
from user.models import UserNormal
from ckeditor.fields import RichTextField
from tag.models import Tag
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete
# Create your models here.


class Article(models.Model):

    title  = models.CharField(max_length=200,verbose_name="Başlık")
    author = models.ForeignKey(UserNormal,on_delete=models.CASCADE,related_name="articles")
    image  = models.ImageField(verbose_name="Resim",blank=True,null=True)
    created_date = models.DateField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")
    content = RichTextField(verbose_name="İçerik")
    tags =models.ManyToManyField(Tag,blank=True,null=True,related_name="article")
    likes =models.ManyToManyField(UserNormal,blank=True,related_name="article_like_list")
    dislikes =models.ManyToManyField(UserNormal,blank=True,related_name="article_dislike_list")
    pageview=models.PositiveIntegerField(default=0)

    is_active=models.BooleanField(default=False,blank=True,verbose_name="Yayınla")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("index")

    def delete(self, *args, **kwargs):
        #self.statistics.delete()
        return super(self.__class__, self).delete(*args, **kwargs)



#If Article deleted, Article's likes will delete
@receiver(post_delete, sender=Article)
def post_delete_likes(sender, instance, *args, **kwargs):
    if instance.likes: # just in case user is not specified
        instance.likes.delete()

#If Article deleted, Article's dislikes will delete
@receiver(post_delete, sender=Article)
def post_delete_dislikes(sender, instance, *args, **kwargs):
    if instance.dislikes: # just in case user is not specified
        instance.dislikes.delete()



class Comment(models.Model):

    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name="comments")
    author  = models.ForeignKey(UserNormal,on_delete=models.CASCADE,related_name="comments")
    created_date =models.DateTimeField(auto_now_add=True)
    content =models.TextField()
    likes = models.ManyToManyField(UserNormal, blank=True, related_name="comment_like_list")
    dislikes = models.ManyToManyField(UserNormal, blank=True, related_name="comment_dislike_list")
    is_positive=models.BooleanField(default=True)



class Reply(models.Model):

    parent=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="replies")
    author =models.ForeignKey(UserNormal)
    created_date=models.DateTimeField(auto_now_add=True)
    content =models.TextField()
    likes = models.ManyToManyField(UserNormal, blank=True, related_name="reply_like_list")
    dislikes = models.ManyToManyField(UserNormal, blank=True, related_name="reply_dislike_list")



class RelatedLink(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE,related_name="related_articles")
    title =models.TextField()
    author=models.ForeignKey(UserNormal,on_delete=models.CASCADE,related_name="related_articles")
    link =models.URLField()
    is_positive =models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title