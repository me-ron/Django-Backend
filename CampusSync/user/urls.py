from .views import UserViewSet, JWTHome, HostViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'hosts', HostViewSet, basename='host')
urlpatterns = router.urls + [
    path('', JWTHome.as_view()),
]
