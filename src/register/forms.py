from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Team

# Extend built-in User form to include email, first name, and last name fields
class ExtendedUserCreationForm(UserCreationForm):
    def validate_email(address):
        if User.objects.filter(email=address).exists():
            raise ValidationError('Email already in use.')
    
    email = forms.EmailField(required=True, validators=[validate_email])
    # name lengths as specified by Django 3.0.* documentation
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
   

class TeamForm(forms.ModelForm):
    name = forms.CharField(max_length=30)

    class Meta:
        model = Team
        fields = ['name', 'division']
        labels = {
            'name': 'Team Name',
        }
        help_texts = {
            'name': '30 characters max. Keep it PG-13 please!',
            'division': 'The division in which your team will compete.',
        }
        error_messages = {
            'name': {
                'max_length': "This team name is too long.",
            },
        }
    
    def clean_name(self):
        reserved_names = ['Walk-in-U', 'Walk-in-L']
        team_name = self.cleaned_data['name']

        for name in reserved_names:
            if name in team_name:
                raise ValidationError('Team name not allowed.')

        return team_name


class InputEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your registered email'}), required=True)
