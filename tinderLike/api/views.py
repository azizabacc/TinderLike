from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from base.models import Users,  Pictures , Likes, Messages
from .serializers import UserSerializer , PictureSerializer, LikeSerializer ,MessageSerializer
from rest_framework import status 
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import IntegrityError  

""" get all users""" 
@api_view(['GET'])
def getUsers(request):
    try:
        items = Users.objects.all()
        person = UserSerializer(items, many=True)
        return Response(person.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"error": "No users found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" add user""" 
@api_view(['POST'])
def addUser(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        return Response({"error": "User with the same email already exists"}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" delete user""" 
@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


""" get user by id""" 
@api_view(['GET'])
def getUsersById(request, user_id):
    try:
        user = get_object_or_404(Users, id=user_id)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
    except Exception as e:
        # user not found
        error_message = "User not found"  
        return Response({"error": error_message}, status=status.HTTP_404_NOT_FOUND)


""" Add picture BY USER ID""" 
@api_view(['POST'])
def addPictureByUserId(request, user_id):
    serializer = PictureSerializer(data=request.data)
    if serializer.is_valid():
        """ if the user with the user_id exists """
        try:
            user = Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return Response({"error": "user doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer.save(id_user=user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    """ if the data validation by the serializer fails """
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" Get pictures  BY USER ID """
@api_view(['GET'])
def getPicturesByUserId(request, user_id):
    try:
        user = get_object_or_404(Users, id=user_id)
        queryset = Pictures.objects.filter(id_user=user_id)
        # if user has not pictures
        if not queryset.exists():
            return Response({"error": "No picture found for this user"}, status=status.HTTP_404_NOT_FOUND)
        
        picture_serializer = PictureSerializer(queryset, many=True)
        return Response(picture_serializer.data)
    
    except Exception as e:
        # user not found
        error_message = "User not found"  
        return Response({"error": error_message}, status=status.HTTP_404_NOT_FOUND)
    

""" get all lilkes""" 
@api_view(['GET'])
def getAllLikes(request):
    try:
        items = Likes.objects.all()
        like = LikeSerializer(items, many=True)
        return Response(like.data)
    except ObjectDoesNotExist:
        return Response({"error": "No likes found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" like someone """
@api_view(['POST'])
def like_user(request, id_user_liker, id_user_liked):
    try:
        # Get id_user_liker and id_user_liked
        user_liker = Users.objects.get(pk=id_user_liker)
        user_liked = Users.objects.get(pk=id_user_liked)
        
        # Check if a like already exists between these users
        existing_like = Likes.objects.filter(id_user_liker=user_liked, id_user_liked=user_liker).first()
        
        if existing_like:
            # If a like already exists, update the match status to 'match'
            existing_like.match = 'match'
            existing_like.save()
        else:
            # If no like exists, create a new like with the match status 'like'
            Likes.objects.create(id_user_liker=user_liker, id_user_liked=user_liked, match='like')
        
        return Response({"message": "User liked successfully"}, status=status.HTTP_200_OK)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

"""dislike someone """
@api_view(['POST'])
def decline_user(request, id_user_liker, id_user_liked):
    try:
        user_liker = Users.objects.get(pk=id_user_liker)
        user_liked = Users.objects.get(pk=id_user_liked)
        
        #check if the inverse relation excites
        existing_like = Likes.objects.filter(id_user_liker=user_liked, id_user_liked=user_liker).first()
  
        if existing_like:
            existing_like.delete()
            return Response({"message": "Like deleted because the 2 persons disliked each others"}, status=status.HTTP_200_OK)


        else:
            # If no like exists, create a new like with the match status 'decline'
            Likes.objects.create(id_user_liker=user_liker, id_user_liked=user_liked, match='decline')
        
        return Response({"message": "User declined successfully"}, status=status.HTTP_200_OK)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
     
"""get all relations for an id """     
@api_view(['GET'])
def getLikesByUserId(request, user_id):
    # likes where either id_user_liker or id_user_liked matches user_id
    likes = Likes.objects.filter(id_user_liker=user_id) | Likes.objects.filter(id_user_liked=user_id)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

""" get all relations for an id who has MATCH as match"""
@api_view(['GET'])
def getMatchesByUserId(request, user_id):
    #all likes where (id_user_liker = user_id OR id_user_liked = user_id) and match = "match"
    likes = Likes.objects.filter(Q(id_user_liker=user_id) | Q(id_user_liked=user_id), match="match")
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)


"""users you can still like or dislike as an user connected"""
@api_view(['GET'])
def profilesFlowByUserId(request, user_id):
    try:
        user = Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    #users who do not appear in Likes table as user_liked
    users_not_in_likes = Users.objects.exclude(
        likes_received__id_user_liker=user
    )
    
    # users who are not associated with user_liker=user in the Likes table or associated with a match
    users_not_associated_with_liker = Users.objects.exclude(
        Q(likes_given__id_user_liked=user, likes_given__match='match')
    )

    # Combine the results of users_not_in_likes and users_not_associated_with_liker
    result_users = users_not_in_likes & users_not_associated_with_liker
    
   	# Exclude the user with user_id from the result
    result_users = result_users.exclude(pk=user_id)
    serializer = UserSerializer(result_users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# display just women
@api_view(['GET'])
def profilesFlowWomenByUserId(request, user_id):
    try:
        user = Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    users_not_in_likes = Users.objects.exclude(
        likes_received__id_user_liker=user
    )
    
    users_not_associated_with_liker = Users.objects.exclude(
        Q(likes_given__id_user_liked=user, likes_given__match='match')
    )

    result_users = users_not_in_likes & users_not_associated_with_liker
    # Filter the result_users to include only users with gender="woman"
    result_users = result_users.filter(gender="woman")
    
    result_users = result_users.exclude(pk=user_id)
    serializer = UserSerializer(result_users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# display just men
@api_view(['GET'])
def profilesFlowMenByUserId(request, user_id):
    try:
        user = Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    users_not_in_likes = Users.objects.exclude(
        likes_received__id_user_liker=user
    )
    
    users_not_associated_with_liker = Users.objects.exclude(
        Q(likes_given__id_user_liked=user, likes_given__match='match')
    )

    result_users = users_not_in_likes & users_not_associated_with_liker
    # Filter the result_users to include only users with gender="woman"
    result_users = result_users.filter(gender="man")
    
    result_users = result_users.exclude(pk=user_id)
    serializer = UserSerializer(result_users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# return the users of a match 
@api_view(['GET'])
def get_users_by_match_id(request, match_id):
    try:
        match = Likes.objects.get(pk=match_id)
        
        # check if the like status is "match"
        if match.match == 'match':
            # get IDs of concerned users
            user_liker_id = match.id_user_liker_id
            user_liked_id = match.id_user_liked_id

            # get these users from the users table
            user_liker = Users.objects.get(pk=user_liker_id)
            user_liked = Users.objects.get(pk=user_liked_id)


            user_liker_data = UserSerializer(user_liker).data
            user_liked_data = UserSerializer(user_liked).data

            return Response({
                "user_liker": user_liker_data,
                "user_liked": user_liked_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Match is not a 'match'"}, status=status.HTTP_400_BAD_REQUEST)

    except Likes.DoesNotExist:
        return Response({"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
""" send message by user and like id  """
@api_view(['POST'])
def send_message(request, id_user, id_like):
    try:
        # check existance
        user = Users.objects.get(pk=id_user)
        like = Likes.objects.get(pk=id_like)

        # Extract from post
        body = request.data.get("body")
        id_user = request.data.get("id_user")
        id_like = request.data.get("id_like")

        # check compatibility
        if id_user != user.id or id_like != like.id:
            return Response({"error": "Mismatch between user and like IDs"}, status=status.HTTP_400_BAD_REQUEST)

        # create message
        message = Messages(body=body, id_user=user, id_like=like)
        message.save()

        return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)

    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Likes.DoesNotExist:
        return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)
    
""" get all messages of a conversation """
@api_view(['GET'])
def get_conversation(request, id_like):
    try:
        # Filter messages by id_like
        messages = Messages.objects.filter(id_like=id_like)
        
        serializer = MessageSerializer(messages, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Messages.DoesNotExist:
        return Response({"error": "Messages not found"}, status=status.HTTP_404_NOT_FOUND)


""" set profile picture by picture_id"""

@api_view(['PATCH'])
def set_profile_picture(request, picture_id):
    try:
        picture = Pictures.objects.get(pk=picture_id)
        
        # update profile with request/ if no request by default profil set to False
        picture.profile = request.data.get('profile', False)
        picture.save()
        
        # update the other profiles of the same user to have just one profile picture
        if picture.profile:
            user_pictures = Pictures.objects.filter(id_user=picture.id_user, profile=True).exclude(pk=picture_id)
            user_pictures.update(profile=False)
        
        return Response({"message": "Profile picture updated successfully"}, status=status.HTTP_200_OK)
    except Pictures.DoesNotExist:
        return Response({"error": "Picture not found"}, status=status.HTTP_404_NOT_FOUND)



""" edit a message"""
@api_view(['PATCH'])
def edit_message(request, message_id):
    try:
        message= Messages.objects.get(pk=message_id)
        
        # update profile with request/ if no request by default profil set to False
        message.body = request.data.get('body')
        message.save()
        
        
        return Response({"message": "Message updated successfully"}, status=status.HTTP_200_OK)
    except Pictures.DoesNotExist:
        return Response({"error": "Mesaage not found"}, status=status.HTTP_404_NOT_FOUND)
    
""" delete a message by id  """
@api_view(['DELETE'])
def delete_message(request, message_id):
    try:
        message = Messages.objects.get(id=message_id)
    except Messages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


""" Dismatch """
@api_view(['DELETE'])
def dismatch(request, user_liker_id, user_liked_id):
    try:
        matching_like = Likes.objects.filter(
            (Q(id_user_liker=user_liker_id, id_user_liked=user_liked_id) | Q(id_user_liked=user_liker_id, id_user_liker=user_liked_id))
            & Q(match='match')
        ).first()

        if not matching_like:
            return Response({"message": "No match found"}, status=status.HTTP_200_OK)

        Likes.objects.filter((Q(id_user_liker=user_liker_id, id_user_liked=user_liked_id) | Q(id_user_liked=user_liker_id, id_user_liker=user_liked_id)) & Q(match='match')).delete()
        
        return Response({"message": "Dismatched successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #get profile picture by user id 
@api_view(['GET'])
def getProfilePictureByUserId(request, user_id):
    try:
        profile_picture = Pictures.objects.get(id_user=user_id, profile=True)

        serializer = PictureSerializer(profile_picture)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pictures.DoesNotExist:
        return Response({"error": "Profil picture not found for this user"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)