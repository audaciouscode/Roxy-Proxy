from django.db import models

class ContactMessage(models.Model):
    sender = models.CharField(max_length=51)
    email = models.EmailField(max_length=512)
    message = models.TextField(max_length=4096)
    sent = models.DateField(auto_now_add=True)
