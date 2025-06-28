from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin 
from django.contrib.auth.views import LogoutView
from . import views
from django.shortcuts import get_object_or_404

urlpatterns = [
    path('',                   views.task_list,    name='task_list'),
    path('add/',               views.add_task,     name='add_task'),
    path('edit/<int:task_id>/',   views.edit_task,    name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task,  name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task,  name='toggle_task'),
    path('status/<int:task_id>/', views.update_status,name='update_status'),
    path('contact/',           views.contact,      name='contact'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('tasks/<int:task_id>/star/', views.toggle_star, name='toggle_star'),

]