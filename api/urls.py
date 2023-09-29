from django.urls import path
from . import views
app_name='api' 

urlpatterns = [
	path('users', views.getUsers),
    path('users/<int:user_id>', views.getUsersById,name='getOneUser'),

    path('users/add', views.addUser, name='addUser'),
    path('users/deleteAccount/<int:user_id>/', views.delete_user,name='deleteUser'),
    
    path('pictures/add/<int:user_id>', views.addPictureByUserId, name="addPicture"),
    path('pictures/profile/<int:picture_id>', views.set_profile_picture, name='setProfilePicture'),
    path('pictures/getPicture/<int:user_id>', views.getPicturesByUserId, name='getPicture'),

    path('Likes/allLikes', views.getAllLikes),
    path('Likes/user/<int:id_user_liker>/likes/<int:id_user_liked>/', views.like_user, name='likeUser'),
    path('Likes/usersMatches/<int:user_id>/', views.getMatchesByUserId, name='myMatches'),
    path('Likes/usersRelation/<int:user_id>',views.getLikesByUserId),
    path('Likes/usersMatched/<int:match_id>',views.get_users_by_match_id, name='usersMatched'),
    path('Likes/user/<int:id_user_liker>/declines/<int:id_user_liked>/', views.decline_user, name='dislikeUser'),
    path('Likes/<int:user_liker_id>/dismatch/<int:user_liked_id>/', views.dismatch),

    path('profilesFlow/<int:user_id>',views.profilesFlowByUserId, name='profilesFlow'),
    path('profilesFlow/women/<int:user_id>',views.profilesFlowWomenByUserId),
    path('profilesFlow/men/<int:user_id>',views.profilesFlowMenByUserId),


    path('chat/<int:id_user>/<int:id_like>/', views.send_message, name='sendMessage'),
    path('chat/<int:message_id>/edit/', views.edit_message),
    path('chat/<int:message_id>/delete/', views.delete_message),

    path('chat/conversation/<int:id_like>/', views.get_conversation, name='conversation'),

	
    

	
]