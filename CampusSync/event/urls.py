from .views import EventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
urlpatterns = router.urls

 