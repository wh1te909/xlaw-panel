from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', views.index, name='adminpanel'),
    path('add/', views.addAdmin, name='add'),
    path('remove/', views.removeAdmin, name='remove'),
    path('logs/<int:admin_id>/', views.adminlogs, name='adminlogs'),
]