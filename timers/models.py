from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TimeTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    total_time = models.IntegerField(default=0)
