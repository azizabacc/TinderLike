from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Users,  Pictures , Likes
from .serializers import UserSerializer , PictureSerializer
from rest_framework import status 

""" get all users""" 
@api_view(['GET'])
def getUsers(request):
	items = Users.objects.all()
	person = UserSerializer(items, many=True)
	return Response(person.data)

""" add user""" 
@api_view(['POST'])
def addUser(request):
	serializer = UserSerializer(data=request.data)
	if serializer.is_valid() :
		serializer.save()
	return Response(serializer.data)

""" delete user""" 
@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = Users.objects.get(id_user=user_id)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


""" get user by id""" 
@api_view(['GET'])
def getUsersById(request, user_id):
    queryset = Users.objects.filter(id_user=user_id)
    users = UserSerializer(queryset, many=True)  
    return Response(users.data)

""" Add picture BY USER ID""" 
@api_view(['POST'])
def addPictureByUserId(request, user_id):
    serializer = PictureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(id_user=user_id)
        return Response(serializer.data)

""" Get pictures  BY USER ID """
@api_view(['GET'])
def getPicturesByUserId(request, user_id):
    queryset = Pictures.objects.filter(id_user=user_id)
    pictures = PictureSerializer(queryset, many=True)
    return Response(pictures.data)