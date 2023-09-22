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
    id_user = request.session.get("id_user")
    
    res = requests.get('http://localhost:8000/apiprofilesFlow/{}'.format(id_user))

    if res.status_code == 200:
        data = json.loads(res.text)

        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'dislike':
                res = requests.post('http://localhost:8000/apiLikes/user/{}/declines/{}/'.format(id_user, data[0]['id']))
            elif action == 'like':
                res = requests.post('http://localhost:8000/apiLikes/user/{}/likes/{}/'.format(id_user, data[0]['id']))

    return render(request, 'like.html', {"profile": data[0]})


def match(request):
	return render(request, 'match.html')

def chat(request):
	return render(request, 'chat.html')

def profile(request):

	return render(request, 'profile.html')

def swagger_ui(request):
	return render(request, 'swagger-ui.html')
