"""Route Configuration"""
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from raterapp.views import login_user, register_user, Games, Categories

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', Games, 'game')
router.register(r'categories', Categories, 'category')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
]
