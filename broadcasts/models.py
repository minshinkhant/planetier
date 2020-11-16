from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka
from planety.models import Planety
from django.contrib.auth import get_user_model
User = get_user_model()


class Broadcast(models.Model):
    user = models.ForeignKey(
        User, related_name='broadcasts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, default='', blank=False)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    planety = models.ForeignKey(
        Planety, related_name='broadcasts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('broadcasts:single',
                       kwargs={"username": self.user.username, "pk": self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
