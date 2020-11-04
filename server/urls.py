"""Route Configuration"""
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from rest_framework import routers
from raterapp.views import login_user, register_user, Games, Categories, Designers, GameReviews

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', Games, 'game')
router.register(r'categories', Categories, 'category')
router.register(r'designers', Designers, 'designer')
router.register(r'reviews', GameReviews, 'review')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
