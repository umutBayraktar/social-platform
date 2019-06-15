from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required

app_name="user"

urlpatterns = [
    url('page/$',UserPage.as_view(),name="user_page"),
    url('profile/$',login_required(Profile.as_view()),name='user_profile'),
    #regex user profil sayfası yapılacak  users/kullanıcı_adı/ şeklinde olacak

    #url("kontrol",girisTest),
]
