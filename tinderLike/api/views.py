from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from base.models import Users,  Pictures , Likes
from .serializers import UserSerializer , PictureSerializer, LikeSerializer
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
     
@api_view(['GET'])
def getLikesByUserId(request, user_id):
    # likes where either id_user_liker or id_user_liked matches user_id
    likes = Likes.objects.filter(id_user_liker=user_id) | Likes.objects.filter(id_user_liked=user_id)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getMatchesByUserId(request, user_id):
    #all likes where (id_user_liker = user_id OR id_user_liked = user_id) and match = "match"
    likes = Likes.objects.filter(Q(id_user_liker=user_id) | Q(id_user_liked=user_id), match="match")
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

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

