from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import requests
import json

# def student_show(request):
#     x = []
#     for i in range(10):
#         x.append(i)
#     return HttpResponse("<h1>DataFlair Django Tutorials</h1>The Digits are {0}".format(x))

def show_user(request):
	res = requests.get("http://localhost:8000")
	response = json.loads(res.text)
	return HttpResponse(format(response))

def show_template(request):
	res = requests.get("http://localhost:8000")
	# print(res.text)
	response = res.text
	print(response)
	return render(request, 'homepage.html', {"response": res})
	# template = loader.get_template('homepage.html')
	# return HttpResponse(template.render(response))
