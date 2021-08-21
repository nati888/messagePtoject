from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
import uuid

from django.db.models import QuerySet


class User(AbstractUser):

    def get_messages_as_receiver(self, seen: bool = None):
        if seen is None:
            return self.receiver_messages.all()

        return self.receiver_messages.filter(seen=seen)


class MessageManager(models.Manager):
    def mark_messages_as_seen(self, messages: QuerySet):
        with transaction.atomic():
            messages.update(seen=True)
            return True


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    sender = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="sender_messages", null=False, blank=False)
    receiver = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="receiver_messages", null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    subject = models.CharField(max_length=255, null=False, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    objects = MessageManager()

    def __str__(self):
        return f"# {self.id} {self.subject}"

    class Meta:
        ordering = ['-creation_date']
        unique_together = [['sender', 'receiver', 'message', 'subject']]
