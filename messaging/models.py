from django.db import models
from users.models import User

class Connection(models.Model):
    user_a = models.ForeignKey(User, related_name="connections_a", on_delete=models.CASCADE)
    user_b = models.ForeignKey(User, related_name="connections_b", on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_a} ↔ {self.user_b}"


class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
