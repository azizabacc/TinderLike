from rest_framework.routers import DefaultRouter
from . import views 

user_router = DefaultRouter()
user_router.register(r'users', views.getUsers)