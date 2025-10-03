import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Extends the built-in Django token generator for use with account activation.
    """

    # Create a token by hashing user's primary key, a timestamp, and their activation status
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()