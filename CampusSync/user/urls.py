from .views import (UserViewSet
                    , JWTHome
                    , HostViewSet
                    , EventViewSet
                    , events_by_host
                    , hosts_under_user
                    , user_following
                    , follow_host
                    , events_rsvpd
                    , questions_by_user)

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
    path('events_by_host/', events_by_host, name='events-by-host'),
    path('hosts_under_user/', hosts_under_user, name='hosts-under-a-user'),
    path('user_following/', user_following, name='user-folowing'),
    path('follow_host/', follow_host, name='follow-host'),
    path('events_rsvpd/', events_rsvpd, name='events-rsvpd'),
    path('questions_by_user/', questions_by_user, name='user-questions'),

]
