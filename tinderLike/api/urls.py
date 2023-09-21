from django.urls import path
from . import views 

urlpatterns = [
	path('users', views.getUsers),
    path('users/<int:user_id>', views.getUsersById),

    path('users/add', views.addUser, name='addUser'),
    path('users/deleteAccount/<int:user_id>/', views.delete_user),
    
    path('pictures/add/<int:user_id>', views.addPictureByUserId),
    path('pictures/profile/<int:picture_id>', views.set_profile_picture),
    path('pictures/getPicture/<int:user_id>', views.getPicturesByUserId),

    path('Likes/allLikes', views.getAllLikes),
    path('Likes/user/<int:id_user_liker>/likes/<int:id_user_liked>/', views.like_user),
    path('Likes/usersMatches/<int:user_id>/', views.getMatchesByUserId),
    path('Likes/usersRelation/<int:user_id>',views.getLikesByUserId),
    path('Likes/usersMatched/<int:match_id>',views.get_users_by_match_id),
    path('Likes/<int:id_user_liker>/declines/<int:id_user_liked>/', views.decline_user),
    path('Likes/<int:user_liker_id>/dismatch/<int:user_liked_id>/', views.dismatch),

    path('profilesFlow/<int:user_id>',views.profilesFlowByUserId),
    path('profilesFlow/women/<int:user_id>',views.profilesFlowWomenByUserId),
    path('profilesFlow/men/<int:user_id>',views.profilesFlowMenByUserId),


    path('chat/<int:id_user>/<int:id_like>/', views.send_message),
    path('chat/<int:message_id>/edit/', views.edit_message),
    path('chat/<int:message_id>/delete/', views.delete_message),

    path('chat/conversation/<int:id_like>/', views.get_conversation),

	
    

	
]