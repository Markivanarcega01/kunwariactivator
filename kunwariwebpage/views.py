from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {
        'name': 'Mark Ivan Arcega',
    }
    return render(request, 'kunwariwebpage/index.html', context)

def login(request):
    return render(request, 'kunwariwebpage/login.html')

def register(request):
    return render(request, 'kunwariwebpage/registration.html')

def forgotpassword(request):
    return render(request, 'kunwariwebpage/forgotpass.html')