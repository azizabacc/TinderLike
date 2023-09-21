from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from .forms import UserCreationForm
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
	# res = requests.get("http://localhost:8000/usersList")
	# # print(res.text)
	# response = res.json()
	# print(response)
	print(request.session.session_key)
	print(request.session.get("id_user"))
	response = "lalalaal"
	return render(request, 'homepage.html', {"response": response})
	# template = loader.get_template('homepage.html')
	# return HttpResponse(template.render(response))


def make_login(request):
	if request.method == 'POST':
		print("caPOST")
		print(request.POST)
		email = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=email, password=password)
		if user is not None:
			print(user.first_name)
			login(request, user)
			request.session["id_user"]=user.first_name
			print('CA CONNECTE')

			return redirect('main')
		else:
			pass
			print(Exception)
			return render(request, 'login.html',{'responses':'no'})

	else:
		return render(request, 'login.html')

def signup(request):
	if request.method == 'POST':
		print("caPOST")
		print(request.POST.get('email'))
		print(request.POST)
		# userData={
		# "name" : request.POST.get('name'),
		# "email" : request.POST.get('email'),
		# "age" : request.POST.get('age'),
		# "rating" : request.POST.get('rating')
		# }
		value = requests.post("http://localhost:8000/apiaddUser", request.POST)
		data = json.loads(value.text)
		print(data.get('id'))
		userData={
		"username" : request.POST.get('email'),
		"email" : request.POST.get('email'),
		"password1" : request.POST.get('password1'),
		"password2" : request.POST.get('password2'),
		"first_name" : data.get('id'),
		}

		form = UserCreationForm(userData)
		if form.is_valid():
			# print(form)
			form.save()
			print("valid")
		else : 
			try : 
				# print(request.POST)
				# print(form)
				print(userData)
				print(form)
				form.save()
				print('not valid')
				# print(form)
			except Exception as e :
			 	print(str(e))
			
			# print(form)
		# username = request.POST['username']
		# password = request.POST['password']
		# user = authenticate(request, username=username, password=password)
		# if user is not None:
		# 	return redirect('main')
		# else:
		# 	pass
		return render(request, 'signup.html')
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
