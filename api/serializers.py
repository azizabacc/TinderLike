from rest_framework import serializers
from base.models import Users, Pictures ,Likes,  Messages


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
