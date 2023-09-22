from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def set_user_role(sender, instance, created, **kwargs):
    if created and not instance.role:
        if instance.is_superuser:
            instance.role = User.ADMIN
        else:
            instance.role = User.CLIENT
        instance.save()