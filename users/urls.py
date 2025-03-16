from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'users'
urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    #path('', RedirectView.as_view(url='login/', permanent=False)),
    path('register/', views.register_user, name="register_user"),
]