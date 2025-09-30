from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from register.tokens import account_activation_token


logger = get_task_logger(__name__)


@shared_task
def send_validation_email(domain, username):
    """
    Celery task to send a validation email during user account creation.

    domain(str): the domain name of the hosting server

    username(str): a user's username 
    """
    
    try:
        user = User.objects.get(username=username)
    except:
        logger.error(f'Failed to send validation email to {username}')
    else:
        subject = 'Activate Your Programming Contest Account'
        message = render_to_string('register/account_activation_email.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        user.email_user(subject, message)

        logger.debug(f'Validation sent to {user.email}')


@shared_task
def send_username_email(email):
    """
    Celery task to email a user their username.

    email(str): the user's registered email address
    """
    
    try:
        user = User.objects.get(email=email)
    except:
        logger.error(f'Username recovery failed for {email}')
    else:
        subject = 'Programming Contest Username Recovery'
        message = render_to_string('register/recover_username_email.html', {
            'user': user,
        })

        user.email_user(subject, message)

        logger.debug(f'Username recovery sent to {email}')
