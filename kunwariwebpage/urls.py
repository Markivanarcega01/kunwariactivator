from django.urls import path
from . import views


app_name = 'kunwariwebpage'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('chatbot/',views.chatbot_view, name='chatbot'),
]