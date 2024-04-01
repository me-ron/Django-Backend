from django.db import models
from event.models import Event
from user.models import User,  Host

# Create your models here.



class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.TextField()
    #  -> one-to-many from User
    asker = models.ForeignKey(User, related_name='forum_question_asker', on_delete=models.CASCADE)
    # answers -> one-to-many to Answer ,, QuestionObj.answer_set.all() -> answers
    is_answered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}"

class Forum(models.Model):
    id = models.IntegerField(primary_key=True)
    # questions -> one-to-many to Question
    questions = models.ForeignKey(Question, related_name='forum_questions', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Main-forum"
    
class EventForum(Forum):
    # event ->one-to-one to Event
    event = models.OneToOneField(Event, on_delete=models.CASCADE) 

    def __str__(self) -> str:
        return f"{self.id}"

class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    answer = models.TextField()
    question = models.ForeignKey(Question, related_name='question_of_answer', on_delete=models.CASCADE)
    # -> one-to-many from User
    answering_user = models.ForeignKey(User, related_name='answering_user', on_delete=models.CASCADE) 
    #  -> one-to-many from Host
    answering_host = models.ForeignKey(Host, related_name='answering_host', on_delete=models.CASCADE) 
    answered_by_host = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}"