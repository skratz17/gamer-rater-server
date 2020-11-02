"""Route Configuration"""
from django.urls import path
from django.conf.urls import include
from raterapp.views import login_user, register_user

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
]
