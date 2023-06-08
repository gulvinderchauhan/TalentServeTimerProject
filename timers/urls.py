from django.urls import path, include
from . import views

app_name = 'timers'

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('start/', views.start, name='start'),
    path('stop/', views.stop, name='stop'),
    path('get_elapsed_time/', views.get_elapsed_time, name='get_elapsed_time'),
]