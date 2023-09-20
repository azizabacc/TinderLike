from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):

    GENDER_CHOICES = [
        ('man', 'Man'),
        ('woman', 'Woman'),
        ('neutral', 'Neutral'),
    ]
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

class Pictures(models.Model):
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    img = models.TextField()
    profile = models.BooleanField()
    
class Likes(models.Model):
    MATCH_CHOICES = [
        ('neutral', 'Neutral'),
        ('like', 'Like'),
        ('decline', 'Decline'),
        ('match', 'Match'),
    ]
    id_user_liker = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='likes_given')
    id_user_liked = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='likes_received')
    match = models.CharField(max_length=10, choices=MATCH_CHOICES, default='neutral')

class Messages(models.Model):
    body = models.TextField()
    id_like = models.ForeignKey(Likes, on_delete=models.CASCADE)

