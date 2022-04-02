from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
# def welcome(request):
#     return HttpResponse('Welcome to my Instagram Page')

def welcome(request):
    return render(request, 'welcome.html')
