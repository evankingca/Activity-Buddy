from django.contrib.auth.models import AbstractUser
from django.db import models

# -------------------------
# User Models
# -------------------------
class User(AbstractUser):
    first_name = None
    last_name = None

    display_name = models.CharField(max_length=100)
    bio_text = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


# -------------------------
# Activity Models
# -------------------------
class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    #postal_codes = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ("user", "activity")

    def __str__(self):
        return f"{self.user} - {self.activity}"


class Preference(models.Model):
    class ExperienceLevel(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    class TrainingStyle(models.TextChoices):
        WEIGHTLIFTING = "weightlifting", "Weightlifting"
        POWERLIFTING = "powerlifting", "Powerlifting"
        BODYBUILDING = "bodybuilding", "Bodybuilding"
        CROSSFIT = "crossfit", "CrossFit"
        CARDIO = "cardio", "Cardio"
        FUNCTIONAL = "functional_fitness", "Functional Fitness"

    class GymFrequency(models.TextChoices):
        LOW = "1_2", "1–2 times/week"
        MEDIUM = "3_4", "3–4 times/week"
        HIGH = "5_plus", "5+ times/week"

    class WorkoutTime(models.TextChoices):
        EARLY_MORNING = "early_morning", "Early Morning"
        MORNING = "morning", "Morning"
        AFTERNOON = "afternoon", "Afternoon"
        EVENING = "evening", "Evening"
        LATE_NIGHT = "late_night", "Late Night"

    user_activity = models.OneToOneField(
        UserActivity,
        on_delete=models.CASCADE,
        related_name="preference",
    )
    experience = models.CharField( max_length=20, choices=ExperienceLevel.choices )
    goals = models.JSONField(default=list)
    training_styles = models.JSONField(default=list)
    gym_frequency = models.CharField( max_length=20, choices=GymFrequency.choices )
    preferred_workout_times = models.JSONField(default=list, blank=True)
    location_ids = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Preferences for {self.user_activity}"


# -------------------------
# Messaging Models
# -------------------------
class Connection(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        BLOCKED = "BLOCKED", "Blocked"

    user_a = models.ForeignKey( User, related_name="connections_a", on_delete=models.CASCADE )
    user_b = models.ForeignKey( User, related_name="connections_b", on_delete=models.CASCADE )
    status = models.CharField( max_length=20, choices=Status.choices, default=Status.PENDING )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_a} ↔ {self.user_b}"



class DirectMessage(models.Model):
    sender = models.ForeignKey( User, related_name="sent_messages", on_delete=models.CASCADE )
    receiver = models.ForeignKey( User, related_name="received_messages", on_delete=models.CASCADE )
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
