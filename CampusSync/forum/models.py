from django.db import models
from event.models import Event
from user.models import User, Host


class Question(models.Model):
    id = models.IntegerField(primary_key=True)

    question = models.TextField()
    author = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE, null=True)
    # author_id = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE, null=False)

    is_answered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)  
    modified_date = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    upvoted_users = models.ManyToManyField(User, related_name='upvoted_question', blank=True)
    downvoted_users = models.ManyToManyField(User, related_name='downvoted_question', blank=True)

    def __str__(self):
        return f"Answer {self.pk}"

    def upvote(self, user):
        if user not in self.upvoted_users.all():

            if user in self.downvoted_users.all():
                self.downvoted_users.remove(user) 
                user.notifications -= 1

            self.upvotes += 1
            self.upvoted_users.add(user)
            
            user.notifications += 1
            self.save()

    def downvote(self, user):
        if user not in self.downvoted_users.all():
            if user in self.upvoted_users.all():
                self.upvoted_users.remove(user)
                user.notifications -= 1
            
            self.downvotes += 1
            self.downvoted_users.add(user)
            
            user.notifications += 1
            self.save()


class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, blank = True, null=True)
    host = models.ForeignKey(Host, related_name='answers', on_delete=models.CASCADE, blank = True, null=True)
    answered_by_host = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default = 0)
    downvotes = models.PositiveIntegerField(default = 0)
    upvoted_users = models.ManyToManyField(User, related_name='upvoted_answer', blank=True)
    downvoted_users = models.ManyToManyField(User, related_name='downvoted_answer', blank=True)


    def __str__(self):
        return f"Answer {self.pk}"

    def upvote(self, user):
        if user not in self.upvoted_users.all():
            if user in self.downvoted_users.all():
                self.downvoted_users.remove(user) 
                user.notifications -= 1

            self.upvotes += 1
            self.upvoted_users.add(user)

            user.notifications += 1
            self.save()

    def downvote(self, user):
        if user not in self.downvoted_users.all():
            if user in self.upvoted_users.all():
                self.upvoted_users.remove(user)
                user.notifications -= 1

            self.downvotes += 1
            self.downvoted_users.add(user)

            user.notifications += 1
            self.save()
