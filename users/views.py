import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
# Create your views here.


# def login_users(request):
#     if 'user' in request.session:
#         return redirect(reverse('kunwariwebpage:index'))
#     if request.method == 'POST':
#         username = request.POST["username"]
#         password = request.POST["password"]
#         db = get_user_model()
#         user = db.objects.filter(username = username, password = password)
#         print(user)
#         if user is not None:
#             request.session['user'] = username
            
#             return redirect(reverse('kunwariwebpage:index'))
#         else:
#             messages.success(request, "Invalid login")
#             return redirect('login')
#     else:
#         return render(request, 'users/login.html')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    try:
        if request.user.is_authenticated:
            return redirect(reverse('kunwariwebpage:index'))

        if request.method == 'POST':
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('kunwariwebpage:index'))
            else:
                return redirect('users:login_user')
        return render(request, 'users/login.html')
    except:
        return JsonResponse({"error": "Login failed"}, status=500)

# def register_users(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         firstname = data['first_name']
#         lastname = data['last_name']
#         username = data['username']
#         email = data['email']
#         password = data['password']
       
#         db = get_user_model()
#         if db.objects.filter(username = username).exists():
#             #messages.error(request, "Username already exists")
#             #return redirect(reverse('users:register_user'))
#             return JsonResponse({"error": "Username already exists"}, status=400)
#         else:
#             user = db.objects.create_user(
#                 username = username,
#                 email = email,
#                 password = password,
#                 first_name = firstname,
#                 last_name = lastname,
#             )
#             user.save()
#             request.session['user'] = username
#             return JsonResponse({"success": "User created successfully"}, status=200)
#             #return redirect(reverse('kunwariwebpage:index'))
#     else:
#         return render(request, 'users/login.html')
    
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            firstname = data.get('first_name')
            lastname = data.get('last_name')
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            User = get_user_model()

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname
            )

            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return JsonResponse({"success": True, "redirect_url": reverse('kunwariwebpage:index')})
            else:
                return JsonResponse({"error": "Authentication failed after registration"}, status=500)

        except Exception as e:
            return JsonResponse({"error": f"Registration failed: {str(e)}"}, status=400)
        # except KeyError as e:
        #     return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)

    else:
        return render(request, 'users/register.html')  # You can create a separate register page if needed
    
# def logouts(request):
#     try:
#         del request.session['user']
#         #return redirect(reverse('users:login_user'))
#         return render(request, 'users/login.html')
#     except:
#         return redirect(reverse('kunwariwebpage:index'))
    
def logout_user(request):
    try:
        logout(request)
        return redirect(reverse('users:login_user'))
    except:
        return JsonResponse({"error": "Logout failed"}, status=500)

    

# def accounts(request):
#     try:
#         db = get_user_model()
#         users = db.objects.all()
#         return render(request, 'users/accounts.html', {"users": users})
#     except:
#         pass