from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tasks import views as task_views
from tasks.views import signup_view, custom_logout_view  # ✅ added custom logout view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('', task_views.task_list, name='home'),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True,
            next_page='/tasks/'
        ),
        name='login'
    ),

    path('logout/', custom_logout_view, name='logout'),

    path('accounts/signup/', signup_view, name='signup'),
]
