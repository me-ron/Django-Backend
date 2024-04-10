from .views import UserViewSet, JWTHome, HostViewSet, EventViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'hosts', HostViewSet, basename='host')

nested = NestedDefaultRouter(router, r'hosts', lookup='host')
nested.register(r'events', EventViewSet, basename='event')

urlpatterns = router.urls + nested.urls +[
    path('', JWTHome.as_view()),
]
