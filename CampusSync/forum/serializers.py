from rest_framework import serializers
from .models import Question, Answer
from user.serializer import UserSerializer
from user.models import User

class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)

class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='author', write_only=True)
    id = serializers.IntegerField(
        read_only=True,
        )
    # author = RelatedFieldAlternative(queryset=User.objects.all(), serializer=UserSerializer)

    class Meta:
        model = Question
        exclude = ['upvoted_users', 'downvoted_users']
        # fields = ['id', 'question','author_id', 'author', 'is_answered', 'created_date', 'modified_date', 'upvotes', 'downvotes']
        # fields = "__all__"
        # depth = 1

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['author'] = UserSerializer(instance.author).data
    #     return response

class AnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = Answer
        exclude = []
                # fields = ['id', 'answer', 'question', 'user', 'host', 'answered_by_host', 'upvotes', 'downvotes']
