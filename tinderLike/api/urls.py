from django.urls import path
from . import views 

urlpatterns = [
	path('usersList', views.getUsers),
    path('users/<int:user_id>', views.getUsersById),
    path('addUser', views.addUser),
    path('deleteAccount/<int:user_id>/', views.delete_user),
    path('addPicture/<int:user_id>', views.addPictureByUserId),
    path('getPicture/<int:user_id>', views.getPicturesByUserId)

]