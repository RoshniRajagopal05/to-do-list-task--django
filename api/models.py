from django.db import models
from django.contrib.auth.models import User

def create_superuser(self, email, password):
    user = self.create_user(email, password)
    user.is_admin = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

# Task Model
class Task(models.Model):
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # optional
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ new field
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# ✅ NEW: Track user actions (usage stats)
class UserActionLog(models.Model):
    ACTION_CHOICES = [
        ("add", "Added Task"),
        ("delete", "Deleted Task"),
        ("complete", "Completed Task"),
        ("edit", "Edited Task"),
        ("import", "Imported Tasks"),
        ("export", "Exported Tasks"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
    

from django.db import models
from django.contrib.auth.models import User
from .models import Task

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_sent = models.BooleanField(default=False)   # whether frontend already fetched it
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.user.username}: {self.message}"


