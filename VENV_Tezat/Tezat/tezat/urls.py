"""tezat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import Timeline
from user.views import loginprocess,logoutprocess,activate
from django.contrib.auth.views import password_reset,password_reset_done,password_reset_confirm,password_reset_complete
from user.views import Registration
import notifications.urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',Timeline.as_view(),name="index"),
    url(r'^users/',include('user.urls')),
    url(r'^articles/',include('article.urls')),
    url(r'accounts/login/$',loginprocess,name="login"),
    url(r'accounts/logout/$',logoutprocess,name="logout"),
    url(r'^accounts/password/reset/$', password_reset, {'post_reset_redirect': '/accounts/password/reset/done/'},
        name='password_reset'),
    url(r'^accounts/password/reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, {'post_reset_redirect': '/accounts/password/done/'}, name='password_reset_confirm'),
    url(r'^accounts/password/done/$', password_reset_complete, name='password_reset_complete'),
    url('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url('^api/',include("rest_api.urls"),name="rest_api"),
    url(r'^register/',Registration.as_view(),name="registration"),

    url(r'^discussions/',include("discussion.urls")),
    url(r'^tags',include("tag.urls"),name="tag"),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


