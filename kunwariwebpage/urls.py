from django.urls import path
from . import views


app_name = 'kunwariwebpage'
urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/',views.chatbot_view, name='chatbot'),
    path('generate_pptx/', views.generate_pptx, name='generate_pptx'),
]