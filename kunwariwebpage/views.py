from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {
        'name': 'Mark Ivan Arcega',
    }
    return render(request, 'kunwariwebpage/index.html', context)