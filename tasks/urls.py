from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin 
from django.contrib.auth.views import LogoutView
from . import views
from django.shortcuts import get_object_or_404





urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('contact/', views.contact, name='contact'),

]

