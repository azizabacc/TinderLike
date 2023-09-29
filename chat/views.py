from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.views.decorators import gzip
import cv2
import requests
import json
import time

# Create your views here.
# chat/views.py



# def index(request):
#     return render(request, "chat/index.html")

def room(request, room_name):
    id_user = request.session.get('id_user')
    url=request.build_absolute_uri(reverse('api:conversation', args=[room_name]))
    res = requests.get(url)
    chat_messages = json.loads(res.text)

    urlUsers =request.build_absolute_uri(reverse('api:usersMatched', args=[room_name]))
    resUsers= requests.get(urlUsers)
    dataUsers = json.loads(resUsers.text)
    print("ici")
    print(type(id_user))
    print(type(dataUsers["user_liker"]["id"]))
    print(dataUsers["user_liked"]["id"])
    if str(dataUsers["user_liker"]["id"]) == id_user :
      me = dataUsers["user_liker"]["id"]
      he = dataUsers["user_liked"]["id"]
      hisName =dataUsers["user_liked"]["name"]

      myurl=request.build_absolute_uri(reverse('api:getPicture', args=[dataUsers["user_liker"]["id"]]))
      Pic1 = requests.get(myurl)
      myPic = json.loads(Pic1.text)  

      picUrl=request.build_absolute_uri(reverse('api:getPicture', args=[dataUsers["user_liked"]["id"]]))
      resPic = requests.get(picUrl)
      hisPic = json.loads(resPic.text) 
    else:
      me = dataUsers["user_liked"]["id"]
      he = dataUsers["user_liker"]["id"]
      hisName =dataUsers["user_liker"]["name"]
      picUrl=request.build_absolute_uri(reverse('api:getPicture', args=[dataUsers["user_liker"]["id"]]))
      resPic = requests.get(picUrl)
      hisPic= json.loads(resPic.text)  

      myurl=request.build_absolute_uri(reverse('api:getPicture', args=[dataUsers["user_liked"]["id"]]))
      Pic1 = requests.get(myurl)
      myPic = json.loads(Pic1.text) 
    return render(request, 'chat/room.html', {"chat_messages": chat_messages, "room_name": room_name, "id_user": id_user, "users":{"me":str(me),"myPic":myPic,"he":str(he),"hisPic":hisPic,"hisName":hisName} })