from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from manager.models import Profile
from register.models import Team


class UserForm(forms.ModelForm):
    """
    Form to edit a user's name or email address.
    """

    first_name = forms.CharField(
        required=True, max_length=30, help_text='30 characters max')
    last_name = forms.CharField(
        required=True, max_length=150, help_text='150 characters max')
    email = forms.EmailField(help_text='Does NOT need to be your FSU email')


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if email address is attached to an existing user
        if User.objects.filter(email=email).exists():
            try:
                user = User.objects.get(email=email)
            except:
                raise ValidationError('Unable to validate email.')
            else:
                # Email address associated with another account
                if user.username != self.user.username:
                    raise ValidationError('Email already in use.')
                # Email address associated with user's account    
                else:
                    return email
        return email
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        help_texts = {
            'first_name': '30 Characters max',
            'last_name': '150 Characters max',
            'email': 'Does NOT need to be your FSU email',
        }


class ProfileForm(forms.ModelForm):
    """
    Form to edit a user's FSU credentials and email opt-out.
    """

    class Meta:
        EMAIL_CHOICES = (
            (False, 'Opt-in'),
            (True, 'Opt-out'),
        )   
        model = Profile
        fields = ('fsu_id', 'fsu_num', 'announcement_email_opt_out')
        labels = {
            'fsu_id': 'FSU ID',
            'fsu_num': 'FSU number',
            'announcement_email_opt_out': 'Announcement Emails',
        }
        help_texts = {
            'fsu_id': 'Excluding @fsu.edu ex: ab12c@fsu.edu -> ab12c',
            'fsu_num': 'Last 8 numbers on FSUCard. Exclude spaces.',
            'announcement_email_opt_out': 'Contest announcements delivered to your inbox.',
        }
        error_messages = {
            'fsu_id': {
                'max_length': "The id entered is too long.",
            },
            'fsu_num': {
                'max_length': "The number entered is too long.",
            },
        }
        widgets = {'announcement_email_opt_out': forms.Select(choices=EMAIL_CHOICES)}

    """
    Hack to populate the form with the existing FSU number.
        - the fsu_num model field uses the hashid package and doesn't decrypt automatically for typical form populating
    """
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance.fsu_num:
            self.fields['fsu_num'] = forms.IntegerField(max_value=99999999, help_text='Last 8 numbers on FSUCard. Exclude spaces.', label='FSU Number', widget=forms.NumberInput(attrs={'placeholder': str(self.instance.fsu_num.id).zfill(8), }))
            self.fields['fsu_num'].required = False
        else: # Use empty placeholder if the field is blank
            self.fields['fsu_num'] = forms.IntegerField(max_value=99999999, help_text='Last 8 numbers on FSUCard. Exclude spaces.', label='FSU Number', widget=forms.NumberInput(
                attrs={'placeholder': '', }))
            self.fields['fsu_num'].required = False
        

class CourseForm(forms.ModelForm):
    """
    Form to select extra credit courses.
    """
    
    class Meta:
        model = Profile
        fields = ('courses',)
        widgets = {'courses': forms.CheckboxSelectMultiple()}
        help_texts = {
            'courses': 'Select any course above in which you are currently registered.',
        }


class TeamForm(forms.ModelForm):
    """
    Form to update team information.
    """
    
    class Meta:
        model = Team
        fields = ('name', 'division')
        help_texts = {
            'name': '30 characters max. Keep it PG-13 please!',
            'division': 'The division in which your team will compete.',
        }

    # Automatically check team name entry against reserved names
    def clean_name(self):
        reserved_names = ['Walk-in-U', 'Walk-in-L']
        team_name = self.cleaned_data['name']

        for name in reserved_names:
            if name in team_name:
                raise ValidationError('Team name not allowed.')

        return team_name


class JoinForm(forms.Form):
    """
    Form to join an existing team.
    """
    
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='Registered Teams',
        help_text='Team : Division [U/L]')
    pin = forms.CharField(
        max_length=6,
        label='PIN',
        help_text='Ask team admin for PIN')

