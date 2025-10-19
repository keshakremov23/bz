from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('sector/<slug:slug>/', views.sector_detail, name='sector_detail'),
    path('sector/<slug:sector_slug>/lang/<int:lang_number>/', views.lang_detail, name='lang_detail'),
    path('sector/<slug:sector_slug>/lang/<int:lang_number>/topic/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
    path('thetopic/<int:pk>/', views.thetopic_detail, name='thetopic_detail'),
    path('sector/<slug:sector_slug>/lang/<int:lang_number>/topic/<slug:topic_slug>/test/', views.topic_test, name='topic_test'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]