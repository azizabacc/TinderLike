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

	print(request.session.get("id_user"))
	response = "lalalaal"
	return render(request, 'homepage.html', {"response": response})
	# template = loader.get_template('homepage.html')
	# return HttpResponse(template.render(response))


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
	form = UserCreationForm(request.POST)
	if request.method == 'POST':

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
		if form.is_valid():
			form.save()
		else : 
			return render(request, 'signup.html', {"message": str(Exception)})
	else:
		return render(request, 'signup.html')



def like(request):
	return render(request, 'like.html')

def match(request):
	return render(request, 'match.html')

def chat(request):
	return render(request, 'chat.html')

def profile(request):
	return render(request, 'profile.html')

def swagger_ui(request):
	return render(request, 'swagger-ui.html')
