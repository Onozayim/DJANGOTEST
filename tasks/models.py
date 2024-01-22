from django.db import models
from django.contrib.auth.models import User
from assignments.models import Assignment
from django.core.validators import MinLengthValidator


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, validators=[MinLengthValidator(5)])
    description = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    task_exp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)
