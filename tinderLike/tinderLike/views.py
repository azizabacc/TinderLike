from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from .forms import UserCreationForm
from django.contrib import messages
import requests
import json


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
				value = requests.post("http://localhost:8000/apiusers/add", request.POST)
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
	if request.method == 'POST' :
		print(request.POST.get('action'))
		if request.POST.get("action")=='dislike' : 
			print(request.POST.get('action'))
			id_user = request.session.get("id_user")
			res = requests.get('http://localhost:8000/apiprofilesFlow/{}'.format(id_user))
			data = json.loads(res.text)
			return render(request, 'like.html',{"profile" : data[0]})
			# requests.POST('http://localhost:8000/apiprofilesFlow/{}'.format())
		else :
			print(request.POST.get("action"))
			id_user = request.session.get("id_user")
			res = requests.get('http://localhost:8000/apiprofilesFlow/{}'.format(id_user))
			data = json.loads(res.text)
			return render(request, 'like.html',{"profile" : data[0]})
	else : 
		id_user = request.session.get("id_user")
		res = requests.get('http://localhost:8000/apiprofilesFlow/{}'.format(id_user))
		data = json.loads(res.text)
		return render(request, 'like.html', {"profile" : data[0]})

def match(request):
	return render(request, 'match.html')

def chat(request):
	return render(request, 'chat.html')

def profile(request):
	id_user = request.session.get("id_user")
	if request.method == 'POST' and request.POST.get('addPicture') is not None  :
		res = requests.post('http://localhost:8000/apipictures/add/{}'.format(id_user))
		return redirect('profile')
	else :	
		res = requests.get('http://localhost:8000/apiusers/{}'.format(id_user))
		data = json.loads(res.text)
		resPicture = requests.get('http://localhost:8000/apipictures/getPicture/{}'.format(id_user))
		if resPicture : 
			dataPicture=json.load(resPicture)
			print(dataPicture)
			return render(request, 'profile.html',{"my_user": data , "my_picture" : dataPicture})
			print(data)
		else :
			return render(request, 'profile.html',{"my_user": data})

def swagger_ui(request):
	return render(request, 'swagger-ui.html')
