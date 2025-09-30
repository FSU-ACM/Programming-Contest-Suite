from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.db import transaction
# from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from contestadmin.models import Contest
from contestsuite.settings import CACHE_TIMEOUT
from core.utils import make_random_password
from manager.utils import has_no_team, not_registered
from register import forms
from register import tasks
from register.tokens import account_activation_token


class ActivateAccount(View):
    """
    View to activate an account after email verification.
    """

    def get(self, request, uidb64, token):
        try:
            # Decode username and check for account
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            # Activate account
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            
            login(request, user)
            messages.success(request, ('Your account has been confirmed!'))
            return redirect('manage_dashboard')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('index')


def base(request):
    return render(request, 'register/register.html')


@user_passes_test(not_registered, login_url='/manage/')
@transaction.atomic
def account(request):
    """
    View to create a user account. Limit view to those who are not logged in. Others redirected to manage.
    """
    
    context = {}

    if request.method == 'POST':
        form = forms.ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.is_active = False # Deactivate account until it is validated
            user.save()

            current_site = get_current_site(request)
            tasks.send_validation_email.delay(current_site.domain, user.username)

            messages.success(
                request, 'Account created! Please check your inbox for an account activation email.')
            messages.info(
                request, 'If your activation email does not arrive in the next few minutes, please check your spam/junk email folder. Head over to our Contact Us page if you need additional help.')
            return redirect('login')

        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True)
    else:
        form = forms.ExtendedUserCreationForm()

    context['page_title'] = 'Contest Registration'
    context['heading'] = 'Contest'
    context['form'] = form
    return render(request, 'register/register_form.html', context)


# key error on password1, more research required
'''def group(request):
    context = {}
    UserFormSet = formset_factory(forms.ExtendedUserCreationForm, extra=3)
    
    if request.method == 'POST':
        formset = UserFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    new_user = User(
                        first_name=form.cleaned_data['first_name'], 
                        last_name=form.cleaned_data['last_name'],
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password1']
                    )
                    # new_user = form.save(commit=False)
                    # new_user.password = form.cleaned_data['password1']
                    new_user.save()
            
            messages.success(
                request, 'Accounts registered!')
            return redirect('index')
        
        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True)
    else:
        formset = UserFormSet()

    context['formset'] = formset
    return render(request, 'register/group_register_form.html', {'formset': formset})'''


@login_required
@user_passes_test(has_no_team, login_url='/manage/')
@transaction.atomic
def team(request):
    """
    View to create a team. Limit view to those are not on a team. Others redirected to manage.
    """
    
    context = {}

    contest = cache.get_or_set(
        'contest_model', Contest.objects.first(), CACHE_TIMEOUT)
    
    # Enforce registration deadline
    if contest and contest.team_deadline and timezone.now() > contest.team_deadline:
        messages.error(
            request, 'Team registration closed. The registration deadline has already passed.', fail_silently=True)
        return redirect('manage_dashboard')

    if request.method == 'POST':
        form = forms.TeamForm(request.POST)
        if form.is_valid():
            # Create a temporary object, add additional attribute data, then save to DB
            newTeam = form.save(commit=False)
            newTeam.pin = make_random_password(length=6)
            newTeam.num_members += 1
            newTeam.save()

            # Update user profile with new team
            request.user.profile.team = newTeam
            request.user.profile.team_admin = True
            request.user.profile.save()
            
            messages.success(
                request, 'Team registered!', fail_silently=True)
            return redirect('manage_dashboard')

        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True)
    else:
        form = forms.TeamForm()

    context['page_title'] = 'Team Registration'
    context['heading'] = 'Team'
    context['form'] = form
    return render(request, 'register/register_form.html', context)


def recover_username(request):
    """
    View to recover a user's username.
    """
    
    context = {}

    if request.method == 'POST':
        form = forms.InputEmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            tasks.send_username_email.delay(email)

            messages.info(
                request, 'If the address you entered is attached to an account, you will receive an email with your username.', fail_silently=True)
            return redirect('recover_username')
        else:
            messages.error(
                request, 'Please correct the error(s) below.', fail_silently=True)
    else:
        form = forms.InputEmailForm()

    context['form'] = form

    return render(request, 'register/recover_username_form.html', context)
