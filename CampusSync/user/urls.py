from .views import UserViewSet, JWTHome
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls + [
    path('', JWTHome.as_view()),
]

# urlpatterns = 