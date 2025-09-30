from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.template.loader import render_to_string


logger = get_task_logger(__name__)


@shared_task
def send_credentials(username):
    """
    Celery task to email a checked-in contestant their DOMjudge credentials.

    username(str): the user's registration suite account username
    """
    
    user = User.objects.get(username=username)
    
    subject = 'Programming Contest DOMjudge Credentials'
    message = render_to_string('checkin/team_credentials_email.html', {'user': user})
    user.email_user(subject, message)

    logger.debug(f'Sent credentials to {username}')
