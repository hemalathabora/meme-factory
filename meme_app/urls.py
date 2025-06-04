from django.urls import path
from . import views

urlpatterns = [
    path('', views.meme_home, name='meme_home'),
]
