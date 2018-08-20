from django.urls import path
from . import views

urlpatterns = [
    path('unique/', views.uniquePlayers),
    path('stats/<steamid>/', views.playerStats),
    path('chat/<steamid>/', views.chatHistory),
    path('topserver/', views.topServer),
    path('topmap/', views.topMap),
    path('totalhoursplayed/', views.totalHours),
    path('topten/', views.topTen),
]