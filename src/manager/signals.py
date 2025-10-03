from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from manager.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal which runs whenever a User object is saved in the database.
    https://docs.djangoproject.com/en/4.2/ref/signals/#post-save
    """

    # Only create a Profile object if the User object is new
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal which runs whenever a User object is saved in the database.
    https://docs.djangoproject.com/en/4.2/ref/signals/#post-save
    """
    
    # Automatically assign 'Admin' role to Profile if user is a superuser
    if instance.is_superuser:
        instance.profile.role = 5
    instance.profile.save()

