from django.db import models
from event.models import Event
from user.models import User, Host

class Question(models.Model):
    question = models.TextField()
    author = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE, null=True)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Question {self.pk}"

class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, null=True)
    host = models.ForeignKey(Host, related_name='answers', on_delete=models.CASCADE, null=True)
    answered_by_host = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer {self.pk}"
