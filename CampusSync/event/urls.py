from .views import EventViewSet, event_notifications, search, order_by_old, order_by_downvote,order_by_recent,order_by_upvote
from .views import EventViewSet, event_notifications, event_search

from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
urlpatterns =  router.urls + [
    path('event-notifications/', event_notifications),
    path('event-search/', search),
    path('event-order-recent/', order_by_recent),
    path('event-order-upvote/', order_by_upvote),
    path('event-order-downvote/', order_by_downvote),
    path('event-order-old/', order_by_old),

  path('event-search/', event_search),
    # # Assuming 'events/' is the base URL for EventViewSet
    # path('events/', EventViewSet.as_view({'get': 'list', 'post': 'create'}), name='event-list'),
    # # Add a URL pattern that includes the pk for detail views
    # path('events/<int:pk>/', EventViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='event-detail'),
    # # Additional URL patterns for other views if needed

]

 