from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from register.models import Team


class ExtendedUserCreationForm(UserCreationForm):
    """
    Extend built-in User form to include email, first name, and last name fields
    Update 02/20/2026: also includes check for passed_cop3330 field
    """
    
    def validate_email(address):
        if User.objects.filter(email=address).exists():
            raise ValidationError('Email already in use.')
    
    email = forms.EmailField(required=True, validators=[validate_email])
    # name lengths as specified by Django 3.0.* documentation
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    PASSED_COP3330_CHOICES = (
        (True, 'Yes'), 
        (False, 'No')
    )

    passed_cop3330 = forms.TypedChoiceField(
        choices=PASSED_COP3330_CHOICES,
        label='Have you passed COP3330?',
        help_text='Check this if you have passed COP3330, or you are a graduate CS student, CS faculty member, or an experienced programmer.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'passed_cop3330', 'password1', 'password2']
   

class TeamForm(forms.ModelForm):
    """
    Form to create a contest team.
    """
    
    class Meta:
        model = Team
        fields = ['name']
        help_texts = {
            'name': '30 characters max. Keep it PG-13 please!',
        }
        error_messages = {
            'name': {
                'max_length': "This team name is too long.",
            },
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Your team's name"}),
        }

    
    # Automatically check team name entry against reserved names
    def clean_name(self):
        reserved_names = ['Walk-in-U', 'Walk-in-L']
        team_name = self.cleaned_data['name']

        for name in reserved_names:
            if name in team_name:
                raise ValidationError('Team name not allowed.')

        return team_name


class InputEmailForm(forms.Form):
    """
    Form to enter an email address. Used during username recovery process.
    """

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your registered email'}), required=True)
