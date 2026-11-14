from django import forms

from lfg.models import LFGProfile


class ProfileForm(forms.ModelForm):
    """
    Form for LFG profile creation.

    division - a contestant's preferred division (Lower/Upper)
    standing - a contestants collegiate standing(Other, Freshman -> Senior, Graduate)

    *** IMPORTANT Dec 2023 *** Discord has updated their username format and
    no longer utilizes discriminators. This form MUST be updated to support
    the new format.

    discord_username
    discord_discriminator
    ***
    """
    
    class Meta:
        model = LFGProfile
        fields = ('discord_username', 'division', 'standing')
        labels = {
            'discord_username': 'Discord Username', 
            'division': 'Preferred Division', 
            'standing': 'Standing',
        }
        help_texts = {
            'discord_username': 'Your username.',
            'division': 'The division in which you intend to compete.', 
        }
        error_messages = {
            'discord_username': {
                'max_length': "The username entered is too long.",
            },
        }
