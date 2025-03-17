from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
#from django.contrib.auth.models import User
#from users.models import NewUser
from django.contrib.auth import get_user_model

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username =username, password = password)

        if user is not None:
            login(request, user)
            return redirect(reverse('kunwariwebpage:index'))
        else:
            messages.success(request, "Invalid login")
            return redirect('login')
    else:
        return render(request, 'users/login.html')

def register_user(request):
    if request.method == 'POST':
        firstname = request.POST["register-firstname"]
        lastname = request.POST["register-lastname"]
        username = request.POST["register-username"]
        email = request.POST["register-email"]
        password = request.POST["register-password"]

        db = get_user_model()
        user = db.objects.create_user(
            username = username,
            password = password,
            email = email,
            first_name = firstname,
            last_name = lastname,
        )
        user.save()
        return redirect(reverse('kunwariwebpage:index'))
    else:
        return render(request, 'users/login.html')