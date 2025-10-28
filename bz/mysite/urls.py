from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from bazaznaniy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', views.custom_logout, name='custom_logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', include('bazaznaniy.urls')),
]