from django.urls import path
from . import views


app_name = 'kunwariwebpage'
urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/',views.chatbot_view, name='chatbot'),
    path('generate_episodes/', views.generate_episodes, name='generate_episodes'),
    path('generate_content/', views.generate_content, name='generate_content'),
    path('generate_facilitator_script/', views.generate_facilitator_script, name='generate_facilitator_script'),
    path('generate_pptx/', views.generate_pptx, name='generate_pptx'),
    path('download/', views.download_from_media, name="download"),
]