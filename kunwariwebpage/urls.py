from django.urls import path
from . import views


app_name = 'kunwariwebpage'
urlpatterns = [
    path('', views.index, name='index'),
]