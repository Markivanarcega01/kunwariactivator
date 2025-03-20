from django.urls import path
from . import views

app_name = 'pricings'
urlpatterns = [
    path('',views.pricing_list, name='pricing_list'),
]
