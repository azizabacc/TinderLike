"""
URL configuration for tinderLike project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from rest_framework import permissions
from django.views.generic import TemplateView
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TinderLike",
        default_version='v1',
        description="API for a dating app like Tinder",
        github={
            "repository_url": "https://github.com/azizabacc/TinderLike",
       
        },
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include('api.urls')),
    path("chat/", include("chat.urls")),
    path('test', views.show_user),
    path('', views.show_template, name='main'),
    path('login',views.make_login, name='login'),
    path('signup',views.signup, name='signup'),
    path('profile',views.profile, name='profile'),
    path('match',views.match, name='match'),
    path('like',views.like, name='like'),
    path('chatting/<int:match_id>',views.chat, name='chat'),
    path('Doc/', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    path('screens/', views.indexscreen, name='screens'),
    re_path(r'^(?P<stream_path>(.*?))/$',views.dynamic_stream,name="videostream"),  
    re_path(r'^stream/$',views.indexscreen),

    ]
