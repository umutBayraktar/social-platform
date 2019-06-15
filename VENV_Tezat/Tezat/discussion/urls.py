from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

app_name="discussion"

urlpatterns=[
    url('discussion/(P?[0-9]+)/$',DetailDiscussion.as_view(),name="discussion_detail"),
    url('list/$',ListAllDiscussions.as_view(),name="list_discussions"),
    url('add',login_required(AddDiscussion.as_view()),name="add_discussion"),


]