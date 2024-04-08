import json
from django.test import TestCase
from rest_framework.test import APIClient
from forum.models import Question, Answer
from forum.serializers import QuestionSerializer

class QuestionViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.question1 = Question.objects.create(question="What is the meaning of life?")
        self.question2 = Question.objects.create(question="How do you like your coffee?")

    def test_list_questions(self):
        response = self.client.get('/questions/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2) 

class AnswerViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.question = Question.objects.create(question="What is the meaning of life?")
        self.answer1 = Answer.objects.create(answer="42 is the answer to everything.", question=self.question)
        self.answer2 = Answer.objects.create(answer="I like my coffee with cream and sugar.", question=self.question)

    def test_list_answers(self):
        response = self.client.get('/answers/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
    
class QuestionSerializerTests(TestCase):
    def test_question_serialization(self):
        question = Question.objects.create(question="What is the meaning of life?")
        serializer = QuestionSerializer(question)
        expected_data = {'id': question.id, 'question': "What is the meaning of life?", 'author': None, 'is_answered': False}
        self.assertEqual(serializer.data, expected_data)

