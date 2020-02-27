"""Music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from app import views as v
from django.conf.urls.static import static
from django.views.static import serve
from Music.settings import MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',v.index),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # path('player/',v.player),
    path('search/',v.search),
    path('person/',v.person),
    path('modify/',v.modify),
    path('imgupload/',v.imgUpload),
    path('login/',v.user_login),
    path('register/',v.register),
    path('comment/',v.comment),
    path('commentlike/',v.commentsLike),
    path('replay/',v.replyComment),
    path('logout/',v.logout),
    path('getcode/',v.get_code),
    re_path("category/(?P<id>\d+)/",v.category),
    re_path("player/(?P<id>\d+)/",v.player),
    path('like/',v.like),
]
