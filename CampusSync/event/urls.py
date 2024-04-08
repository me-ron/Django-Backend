from .views import (
        EventViewSet, search, order_by_old
        , order_by_downvote,order_by_recent
        ,order_by_upvote, CommentCreateView
        ,EventCommentListView
    )

from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
urlpatterns =  router.urls + [
    path('event-order-recent/', order_by_recent),
    path('event-order-upvote/', order_by_upvote),
    path('event-order-downvote/', order_by_downvote),
    path('event-order-old/', order_by_old),
    path('comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('events/<int:event_id>/comments/', EventCommentListView.as_view(), name='event-comments-list'),


]

 