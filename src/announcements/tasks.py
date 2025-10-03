from celery import shared_task
from celery.utils.log import get_task_logger
from discord import SyncWebhook, Embed
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

from announcements.models import Announcement
from contestsuite.settings import ANNOUNCEMENT_WEBHOOK_URL, DEFAULT_FROM_EMAIL, ALLOWED_HOSTS


logger = get_task_logger(__name__)


@shared_task
def email_annoucement(id):
    """
    Celery task to distribute a published announcement to users.

    id: unique database id of the accouncement
    """

    try:
        announcement = Announcement.objects.get(id=id)
    except:
        logger.error(f'Failed to fetch announcement with id {id}')
    else:
        i=0
        users = User.objects.all()
        messages = []
        # Prepare email content
        message = render_to_string(
            'announcements/new_announcement_email.html',
            {'announcement': announcement})
        
        # Prepare email per user
        # Using seperate message per user to avoid address exposure
        for user in users:
            if user.is_active and not user.profile.announcement_email_opt_out:
                i += 1
                messages.append((announcement.title, message, DEFAULT_FROM_EMAIL, [user.email]))

        # send_mass_mail requires Tuple type
        messages = tuple(messages)
        send_mass_mail(messages, fail_silently=False)

        logger.info(f'Sent announcement to {i} users')

@shared_task
def discord_announcement(id):
    """
    Celery task to deliver a published announcement to a Discord webhook.

    id: unique database id of the accouncement
    """

    try:
        announcement = Announcement.objects.get(id=id)
    except:
        logger.error(f'Failed to fetch announcement with id {id}')
    else:
        # Initializing webhook
        webhook = SyncWebhook.from_url(ANNOUNCEMENT_WEBHOOK_URL)
        url = 'https://'+ALLOWED_HOSTS[0]+announcement.get_absolute_url()
        
        if len(announcement.content) <= 140:
            content = announcement.content
        else:
            content = announcement.content[:140] + '...'
        
        # Initializing an Embed
        embed = Embed(title=announcement.title, description=content, url=url)

        # Executing webhook.
        webhook.send(embed=embed)
