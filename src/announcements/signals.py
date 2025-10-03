from django.db.models.signals import post_save
from django.dispatch import receiver

from announcements.models import Announcement
from announcements.tasks import email_annoucement, discord_announcement


@receiver(post_save, sender=Announcement)
def send_announcement(sender, instance, created, **kwargs):
	"""
	Signal which runs whenever an Announcement object is saved in the database.
	Announcement must be 'Published' status to distribute via Discord or email.
	https://docs.djangoproject.com/en/4.2/ref/signals/#post-save
	"""

	# Publish
	if instance.status == 1:
		if instance.send_email:
			email_annoucement.delay(instance.id)
		if instance.send_discord:
			discord_announcement.delay(instance.id)
	# Draft
	else:
		pass
