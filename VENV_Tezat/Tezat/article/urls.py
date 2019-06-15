from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required

app_name="article"

urlpatterns=[
    url('addarticle',login_required(CreateArticle.as_view()),name="article_create"),
    url('updatearticle/(?P<pk>[0-9]+)/$',login_required(UpdateArticle.as_view()),name="article_update"),
    url('deletearticle/(?P<pk>[0-9]+)/$',login_required(DeleteArticle.as_view()),name="article_delete"),
    url('article/(P?[0-9]+)/$',DetailArticle.as_view(),name="article_detail"),
    url('list/$',ListAllArticle.as_view(),name="list_article"),



]