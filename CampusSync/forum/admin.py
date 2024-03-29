from django.contrib import admin
from .models import Question, Forum, EventForum, Answer
# Register your models here.

admin.site.register(Question)
admin.site.register(Forum)
admin.site.register(EventForum)
admin.site.register(Answer)