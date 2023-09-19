from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Users 
from .serializers import UserSerializer

@api_view(['GET'])
def getData(request):
	items = Users.objects.all()
	person = UserSerializer(items, many=True)
	return Response(person.data)

@api_view(['POST'])
def addItem(request):
	serializer = UserSerializer(data=request.data)
	if serializer.is_valid() :
		serializer.save()
	return Response(serializer.data)