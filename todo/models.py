from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'کم'),
        (2, 'متوسط'),
        (3, 'زیاد'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_priority_display(self):
        return self.PRIORITY_CHOICES[self.priority - 1][1]

