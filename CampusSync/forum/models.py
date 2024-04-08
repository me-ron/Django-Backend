from django.db import models
from event.models import Event
from user.models import User, Host


class Question(models.Model):
    question = models.TextField()
    author = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE, null=True)
    is_answered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)  
    modified_date = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    upvoted_users = models.ManyToManyField(User, related_name='upvoted_questions', blank=True)
    downvoted_users = models.ManyToManyField(User, related_name='downvoted_questions', blank=True)

    def __str__(self):
        return f"Answer {self.pk}"

    def upvote(self, user):
        if user not in self.upvoted_users.all():
            self.upvotes += 1
            self.upvoted_users.add(user)
            self.downvoted_users.remove(user)  # Remove user from downvoted list
            self.save()

    def downvote(self, user):
        if user not in self.downvoted_users.all():
            self.downvotes += 1
            self.downvoted_users.add(user)
            self.upvoted_users.remove(user)  # Remove user from upvoted list
            self.save()


class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, blank = True, null=True)
    host = models.ForeignKey(Host, related_name='answers', on_delete=models.CASCADE, blank = True, null=True)
    answered_by_host = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default = 0)
    downvotes = models.PositiveIntegerField(default = 0)
    upvoted_users = models.ManyToManyField(User, related_name='upvoted_answers', blank=True)
    downvoted_users = models.ManyToManyField(User, related_name='downvoted_answers', blank=True)

    def __str__(self):
        return f"Answer {self.pk}"

    def upvote(self, user):
        if user not in self.upvoted_users.all():
            self.upvotes += 1
            self.upvoted_users.add(user)
            self.downvoted_users.remove(user) 
            self.save()

    def downvote(self, user):
        if user not in self.downvoted_users.all():
            self.downvotes += 1
            self.downvoted_users.add(user)
            self.upvoted_users.remove(user)
            self.save()
