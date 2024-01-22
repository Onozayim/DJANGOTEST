from django.db import models
from django.contrib.auth.models import User
import os
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/ass', filename)

class Assignment(models.Model):
    title = models.CharField(max_length=25)
    teacher = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)