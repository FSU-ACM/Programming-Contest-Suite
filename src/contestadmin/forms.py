from django import forms

from contestadmin.models import Contest
from manager.models import Profile


class CheckinUsersForm(forms.Form):
    ACTION = (
        (1, 'Live Checkin'),
        (2, 'Practice Checkin'),
        (3, 'Checkout')
    )

    action = forms.ChoiceField(choices=ACTION)


class GenerateWalkinForm(forms.Form):
    DIVISION = (
        (1, 'Upper Division'),
        (2, 'Lower Division')
    )

    total = forms.IntegerField()
    division = forms.ChoiceField(choices=DIVISION)


class ResultsForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['results']


class ClearChannelForm(forms.Form):
    channel_id = forms.IntegerField()


class UpdateProfileRoleForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Username',
        help_text="Volunteer's account username.")
    class Meta:
        model = Profile
        fields = ["role"]
