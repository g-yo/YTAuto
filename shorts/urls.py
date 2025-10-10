from django.urls import path
from . import views

app_name = 'shorts'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_short, name='generate_short'),
    path('upload/<int:short_id>/', views.upload_to_youtube, name='upload_to_youtube'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('history/', views.history, name='history'),
]
