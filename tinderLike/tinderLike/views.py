from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib import messages
import requests
import json

# def student_show(request):
#     x = []
#     for i in range(10):
#         x.append(i)
#     return HttpResponse("<h1>DataFlair Django Tutorials</h1>The Digits are {0}".format(x))

def show_user(request):
	res = requests.get("http://localhost:8000/usersList")
	response = json.loads(res.text)
	return HttpResponse(format(response))

def show_template(request):
	res = requests.get("http://localhost:8000/usersList")
	# print(res.text)
	response = res.json()
	print(response)
	return render(request, 'homepage.html', {"response": response})
	# template = loader.get_template('homepage.html')
	# return HttpResponse(template.render(response))


def login(request):
	if request.method == 'POST':
		print("caPOST")
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			return redirect('main')
		else:
			pass
			
			return render(request, 'login.html',{'response':'no'})

	else:
		return render(request, 'login.html')

def signup(request):
	if request.method == 'POST':
		print("caPOST")
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			return redirect('main')
		else:
			pass
			return render(request, 'login.html')
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
