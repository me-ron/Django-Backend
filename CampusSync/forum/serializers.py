from rest_framework import serializers
from .models import Question, Answer
from user.serializer import UserSerializer
from user.models import User

class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Question
        fields = ['id', 'question', 'author', 'is_answered', 'created_date', 'modified_date', 'upvotes', 'downvotes']
        # fields = '__all__'
class AnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'answer', 'question', 'user', 'host', 'answered_by_host', 'upvotes', 'downvotes']
