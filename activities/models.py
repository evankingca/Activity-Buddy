from django.db import models
from users.models import User

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    postal_codes = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user} - {self.activity}"


class Preference(models.Model):
    user_activity = models.ForeignKey(UserActivity, on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    memberships = models.CharField(max_length=200)
    goals = models.CharField(max_length=200)

    def __str__(self):
        return f"Preferences for {self.user_activity}"
