from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from .forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.views.decorators import gzip
import cv2
import requests
import json
import time


def show_user(request):
	res = requests.get("http://localhost:8000/usersList")
	response = json.loads(res.text)
	return HttpResponse(format(response))

def show_template(request):
	return render(request, 'homepage.html')



def make_login(request):
	if request.method == 'POST':

		email = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user)
			request.session["id_user"]=user.first_name
			return redirect('main')
		else:
			pass
			print(Exception)
			return render(request, 'login.html',{'responses':'no'})

	else:
		return render(request, 'login.html')

def signup(request):
	if request.method == 'POST' : 
		form = UserCreationForm(request.POST)
		if form.is_valid():
			try : 
				url=request.build_absolute_uri(reverse('api:addUser'))
				value = requests.post(url, request.POST)
				data = json.loads(value.text)
			
				userData={
				"username" : request.POST.get('email'),
				"email" : request.POST.get('email'),
				"password1" : request.POST.get('password1'),
				"password2" : request.POST.get('password2'),
				"first_name" : data.get('id'),
				}

				form = UserCreationForm(userData)
				form.save()
				
				user = authenticate(request, username=userData.get('username'), password=userData.get('password1'), id=data.get('id'))
				print(user)
				if user is not None:
	
					login(request, user)
					request.session["id_user"]=user.first_name


					return redirect('main')
				else : 
					return redirect('login')

			except Exception as error : 
				return render(request, 'signup.html', {"message": form.errors})
		else:

			try :
				form.save()
			except Exception as error : 
				return render(request, 'signup.html',{"message": form.errors})
	else : 
		return render(request, 'signup.html')




def like(request):

	id_user = request.session.get("id_user")
	url=request.build_absolute_uri(reverse('api:profilesFlow', args=[id_user]))
	res = requests.get(url)

	if res.status_code == 200:
		data = json.loads(res.text)
		if request.method == 'POST':
			action = request.POST.get('action')
			if action == 'dislike':
				likeUrl=request.build_absolute_uri(reverse('api:dislikeUser', args=[id_user,data[0]['id']]))
				res = requests.post(likeUrl)
				redirect('like')
			elif action == 'like':
				dislikeUrl=request.build_absolute_uri(reverse('api:likeUser', args=[id_user,data[0]['id']]))
				res = requests.post(dislikeUrl)
				redirect('like')

		picUrl=request.build_absolute_uri(reverse('api:getPicture', args=[data[0].get('id')]))
		resPic = requests.get(picUrl)
		if resPic.status_code == 200 : 

			dataPicture = json.loads(resPic.text)  
			print(dataPicture[0])          
		else : 
			dataPicture = {"img" : 'nopic'}
		return render(request, 'like.html', {"profile": data[0], "picture" : dataPicture})



def match(request):
	id_user= request.session.get('id_user')
	url=request.build_absolute_uri(reverse('api:myMatches', args=[id_user]))
	res = requests.get(url)
	if res.status_code == 200 : 
		data = json.loads(res.text)
		print(data)
		return render(request, 'match.html',{"matches": data})
	else :
		redirect('main')


def chat(request, match_id):
    id_user = request.session.get('id_user')
    url=request.build_absolute_uri(reverse('api:conversation', args=[id_user]))
    res = requests.get(url)
    chat_messages = json.loads(res.text)

    urlUsers =request.build_absolute_uri(reverse('api:usersMatched', args=[match_id]))
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
      hisName =dataUsers["user_liked"]["name"]
      picUrl=request.build_absolute_uri(reverse('api:getPicture', args=[dataUsers["user_liker"]["id"]]))
      resPic = requests.get(picUrl)
      hisPic= json.loads(resPic.text)  

      myurl=request.build_absolute_uri(reverse('api:getPicture', args=[dataUsers["user_liked"]["id"]]))
      Pic1 = requests.get(myurl)
      myPic = json.loads(Pic1.text) 
    
    # if res.status_code == 200:
    #     if request.method == 'POST':
    #         action = request.POST.get('action')
    #         if action == 'send':
    #             message_body = request.POST.get('message') 
    #             print(message_body)
    #             urlChat=request.build_absolute_uri(reverse('api:sendMessage', args=[id_user, match_id]))
    #             res = requests.post(
    #                 ('url'),
    #                 {"body": message_body, "id_user": id_user, "id_like": match_id}
    #             )
    #         elif action == 'delete':
    #             message_id = request.POST.get('message_id')
    #             res = requests.delete(
    #                     'http://localhost:8000/apichat/{}/delete/'.format(message_id)
	# 				)
    #         elif action == 'ok':
    #             message_id = request.POST.get('message_id')
    #             edited_message = request.POST.get('edited_message')
    #             res = requests.patch(
    #                     'http://localhost:8000/apichat/{}/edit/'.format(message_id)
	# 				,{"body": edited_message})
           
    return render(request, 'room.html', {"chat_messages": chat_messages, "obj": match_id, "id_user": id_user, "users":{"me":str(me),"myPic":myPic,"he":str(he),"hisPic":hisPic,"hisName":hisName} })

def profile(request):
	# retrieve user_id
	id_user = request.session.get("id_user")
	# check if you're trying to post a new picture
	if request.method == 'POST' and request.POST.get('addPicture') is not None  :
		# 
		addUrl=request.build_absolute_uri(reverse('api:addPicture', args=[id_user]))
		res = requests.post(addUrl,{'img':request.POST.get('addPicture')})
		return redirect('profile')
	else :	
		url = request.build_absolute_uri(reverse('api:getOneUser', args=[id_user]))
		res = requests.get(url)
		data = json.loads(res.text)
		picUrl = request.build_absolute_uri(reverse('api:getPicture', args=[id_user]))
		resPicture = requests.get(picUrl)
		if resPicture : 
			
			dataPicture=json.loads(resPicture.text)
			
			return render(request, 'profile.html',{"my_user": data , "my_picture" : dataPicture})
			
		else :
			return render(request, 'profile.html',{"my_user": data})

def swagger_ui(request):
	return render(request, 'swagger-ui.html')




def get_frame():
    camera =cv2.VideoCapture(0) #open the webcam video stream (port zero) and enters an infinite loop
    while True:
		#At each iteration of the loop
        _, img = camera.read()# it reads an image from the webcam
        imgencode=cv2.imencode('.jpg',img)[1] # encodes that image in JPEG format
        stringData=imgencode.tostring() #converts it into a byte string 
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')# yield : to send this byte string with specific headers that set the content type. 
    del(camera)#delete it after
    
def indexscreen(request): 
	template = "screens.html"
	return render(request,template)

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")#send data continuously
    except :
        return "error"

