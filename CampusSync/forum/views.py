from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_date')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        q_id = self.kwargs['question_pk']
        return Answer.objects.filter(question=q_id).order_by('-upvotes')