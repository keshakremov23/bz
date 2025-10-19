from django.contrib import admin
from django.urls import path, include
from bazaznaniy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', views.custom_logout, name='custom_logout'),
    path('', include('bazaznaniy.urls')),
]