from django.urls import include, path
from . import views

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter


router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet)

nested = NestedDefaultRouter(router, r'questions', lookup='question')
nested.register(r'answers', views.AnswerViewSet, basename='answer')

urlpatterns = router.urls + nested.urls + [
    path('<int:question_id>/upvote/', views.upvote_question, name='upvote_question'),
    path('<int:question_id>/downvote/', views.downvote_question, name='downvote_question'),
   
]

