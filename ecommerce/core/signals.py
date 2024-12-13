from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from tasks import send_email_task

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Только при создании нового пользователя
        send_email_task.delay(instance.email)
