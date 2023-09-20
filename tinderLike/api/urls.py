from django.urls import path
from . import views 

urlpatterns = [
	path('usersList', views.getUsers),
    path('users/<int:user_id>', views.getUsersById),
    path('addUser', views.addUser),
    path('deleteAccount/<int:user_id>/', views.delete_user),
    
    path('addPicture/<int:user_id>', views.addPictureByUserId),
    path('getPicture/<int:user_id>', views.getPicturesByUserId),
    path('allLikes', views.getAllLikes),
    path('user/<int:id_user_liker>/likes/<int:id_user_liked>/', views.like_user),
    path('usersMatches/<int:user_id>/', views.getMatchesByUserId),
    path('usersRelation/<int:user_id>',views.getLikesByUserId),
    path('profilesFlow/<int:user_id>',views.profilesFlowByUserId),
    path('profilesFlow/women/<int:user_id>',views.profilesFlowWomenByUserId),
    path('profilesFlow/men/<int:user_id>',views.profilesFlowMenByUserId),
	path('usersMatched/<int:match_id>',views.get_users_by_match_id),
    path('user/<int:id_user_liker>/declines/<int:id_user_liked>/', views.decline_user),
    
    path('chat/<int:id_user>/<int:id_like>/', views.send_message),
    path('conversation/<int:id_like>/', views.get_conversation),

	
    

	
]