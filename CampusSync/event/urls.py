from .views import EventViewSet, event_notifications, event_search
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
urlpatterns = router.urls + [
    path('event-notifications/', event_notifications),
    path('event-search/', event_search),
]

 