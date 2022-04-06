from django.db import models
from django.contrib.auth.models import User


#database model for reminder
class Reminder(models.Model):
    title = models.CharField(max_length = 100)
    memo = models.TextField(blank = True)
    created_date = models.DateTimeField(auto_now_add = True)
    reminder_date = models.DateTimeField(null=True, blank = True)
    important = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.title} - created date - {self.created_date}'
