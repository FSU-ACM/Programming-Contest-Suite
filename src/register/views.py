import logging
from functools import partial

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from contestadmin.models import Contest
from contestsuite.settings import CACHE_TIMEOUT
from core.utils import make_random_password
from manager.utils import has_no_team, not_registered
from register import forms, tasks
from register.tokens import account_activation_token


logger = logging.getLogger(__name__)

ACTIVATION_RESEND_COOLDOWN = 60
ACTIVATION_RESEND_MESSAGE = (
    'If that address belongs to an account awaiting activation, '
    'we will send an activation email. Check your spam/junk folder '
    'and wait at least one minute before requesting another email.'
)


class ActivateAccount(View):
    """Activate an account after email verification."""

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()

            login(request, user)
            messages.success(request, 'Your account has been confirmed!')
            return redirect('manage_dashboard')

        messages.warning(
            request,
            'The activation link is invalid or has expired. '
            'You can request another activation email below.',
        )
        return redirect('resend_activation')


def resend_activation(request):
    """Allow users to request another activation email."""
    if request.method == 'POST':
        form = forms.InputEmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(
                email__iexact=email,
                is_active=False,
                profile__email_confirmed=False,
            )
            domain = get_current_site(request).domain

            for user in users:
                cooldown_key = f'activation-resend:{user.pk}'
                if not cache.add(cooldown_key, True, timeout=ACTIVATION_RESEND_COOLDOWN):
                    continue

                try:
                    tasks.send_validation_email.delay(domain, user.username)
                except Exception:
                    cache.delete(cooldown_key)
                    logger.exception(
                        'Could not queue activation email for user %s',
                        user.pk,
                    )

            messages.info(request, ACTIVATION_RESEND_MESSAGE)
            return redirect('resend_activation')
    else:
        form = forms.InputEmailForm()

    return render(
        request,
        'register/resend_activation_form.html',
        {'form': form},
    )


def base(request):
    return render(request, 'register/register.html')


@user_passes_test(not_registered, login_url='/manage/')
@transaction.atomic
def account(request):
    """Create a user account. Redirect logged-in users to manage."""
    context = {}

    if request.method == 'POST':
        form = forms.ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user.profile.passed_cop3330 = form.cleaned_data.get('passed_cop3330')
            user.profile.save()

            current_site = get_current_site(request)
            transaction.on_commit(
                partial(
                    tasks.send_validation_email.delay,
                    current_site.domain,
                    user.username,
                ),
                robust=True,
            )

            messages.success(
                request,
                'Account created! Please check your inbox for an account activation email.',
            )
            messages.info(
                request,
                'If your activation email does not arrive, check your '
                'spam/junk folder or use "Resend activation email" on the login page.',
            )
            return redirect('login')

        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True
        )
    else:
        form = forms.ExtendedUserCreationForm()

    context['page_title'] = 'Contest Registration'
    context['heading'] = 'Contest'
    context['form'] = form
    return render(request, 'register/register_form.html', context)


@user_passes_test(not_registered, login_url='/manage/')
@transaction.atomic
def group(request):
    """Register and verify each account separately on contest day."""
    context = {}
    UserFormSet = formset_factory(
        forms.ExtendedUserCreationForm, extra=3, min_num=1, validate_min=True
    )

    if request.method == 'POST':
        formset = UserFormSet(request.POST)
        if formset.is_valid():
            current_site = get_current_site(request)

            for form in formset:
                if form.cleaned_data:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()

                    transaction.on_commit(
                        partial(
                            tasks.send_validation_email.delay,
                            current_site.domain,
                            user.username,
                        ),
                        robust=True,
                    )

            messages.success(
                request,
                'Accounts registered! Check your email inbox for a verification link.',
            )
            return redirect('register_group')

        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True
        )
    else:
        formset = UserFormSet()

    context['formset'] = formset
    return render(request, 'register/group_register_form.html', context)


@login_required
@user_passes_test(has_no_team, login_url='/manage/')
@transaction.atomic
def team(request):
    """Create a team for a user who is not already on one."""
    context = {}

    contest = cache.get_or_set(
        'contest_model', Contest.objects.first(), CACHE_TIMEOUT
    )

    if contest and contest.team_deadline and timezone.now() > contest.team_deadline:
        messages.error(
            request,
            'Team registration closed. The registration deadline has already passed.',
            fail_silently=True,
        )
        return redirect('manage_dashboard')

    if request.method == 'POST':
        form = forms.TeamForm(request.POST)
        if form.is_valid():
            newTeam = form.save(commit=False)
            newTeam.pin = make_random_password(length=6)
            newTeam.division = 2
            newTeam.num_members += 1
            newTeam.save()

            request.user.profile.team = newTeam
            request.user.profile.team_admin = True
            request.user.profile.save()

            newTeam.update_division()

            messages.success(request, 'Team registered!', fail_silently=True)
            return redirect('manage_dashboard')

        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True
        )
    else:
        form = forms.TeamForm()

    context['page_title'] = 'Team Registration'
    context['heading'] = 'Team'
    context['form'] = form
    return render(request, 'register/register_form.html', context)


def recover_username(request):
    """Email a user their username."""
    context = {}

    if request.method == 'POST':
        form = forms.InputEmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            tasks.send_username_email.delay(email)

            messages.info(
                request,
                'If the address you entered is attached to an account, '
                'you will receive an email with your username.',
                fail_silently=True,
            )
            return redirect('recover_username')

        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True
        )
    else:
        form = forms.InputEmailForm()

    context['form'] = form
    return render(request, 'register/recover_username_form.html', context)
