from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required

app_name="tag"

urlpatterns=[
    url('page/$',TagPage.as_view(),name="tag_page"),
    url('add/$',AddTag.as_view(),name="add_tag"),
]