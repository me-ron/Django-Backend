from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user.models import User

from rest_framework import filters


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_date')
    serializer_class = QuestionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    search_fields = ['question']
    filter_backends = (filters.SearchFilter,)

class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        q_id = self.kwargs['question_pk']
        return Answer.objects.filter(question=q_id).order_by('-upvotes')
    
  
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def upvote_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)

    if request.method == 'POST':
        if 'user_id' not in request.data or not request.data['user_id']:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=request.data['user_id'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


        if user in question.downvoted_users.all():
            question.downvoted_users.remove(user)
            question.downvotes = question.downvoted_users.count()
            

        if user in question.upvoted_users.all():
            question.upvoted_users.remove(user)
            question.upvotes = question.upvoted_users.count()

            question.save()

            return Response({'success': 'Your upvote is removed from this event.'
                            ,'question_id': question_id
                            ,'upvotes': question.upvotes})

        question.upvoted_users.add(user)
        question.upvotes = question.upvoted_users.count()
  
        question.save()

        return Response({'status': 'Upvoted successfully!',
                         'question_id': question_id,
                         'upvotes': question.upvotes})
    else:
        return Response({'error': 'Invalid request method'}, status=405)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def downvote_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)

    if request.method == 'POST':
        if 'user_id' not in request.data or not request.data['user_id']:
            return Response({"user_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=request.data['user_id'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if user in question.upvoted_users.all():
            question.upvoted_users.remove(user)
            question.upvotes = question.upvoted_users.count()
            

        if user in question.downvoted_users.all():
            question.downvoted_users.remove(user)
            question.downvotes = question.downvoted_users.count()

            question.save()

            return Response({'success': 'Your downvote is removed from this event'
                             ,'question_id': question_id
                            ,'downvotes': question.downvotes})

        question.downvoted_users.add(user)
        question.downvotes = question.downvoted_users.count()
  
        question.save()

        return Response({'status': 'Downvoted successfully',
                         'question_id': question_id,
                         'downvotes': question.downvotes})
    else:
        return Response({'error': 'Invalid request method'}, status=405)
