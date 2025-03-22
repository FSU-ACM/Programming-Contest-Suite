from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.db import transaction

from . import forms
from .models import LFGProfile
from .utils import profile_activatable, new_lfg_user, lfg_profile_active, current_lfg_user
from contestadmin.models import Contest
from contestsuite.settings import CACHE_TIMEOUT

# Create your views here.

@login_required
def dashboard(request):
    """
    View for displaying the LFG dashboard. 
    """

    context = {}

    contest = cache.get_or_set('contest_model', Contest.objects.first(), CACHE_TIMEOUT)
    if contest:
        context['lfg_active'] = contest.lfg_active
    else:
        context['lfg_active'] = False

    # Dict mapping of standings Graduate/Senior/Junior/Sophomore/Freshman/Other
    context['standings'] = {standing[0]:standing[1] for standing in LFGProfile.STANDING}
    # Dict mapping of divisions Upper/Lower
    context['divisions'] = {division[0]:division[1] for division in LFGProfile.DIVISION}
    # Gather LFG profiles by division
    context['lfg_upper'] = cache.get_or_set(
        'lfg_dash_users_upper', LFGProfile.objects.filter(active=True).filter(division=1), CACHE_TIMEOUT)
    context['lfg_lower'] = cache.get_or_set(
        'lfg_dash_users_lower', LFGProfile.objects.filter(active=True).filter(division=2), CACHE_TIMEOUT)
    # LFG Profile counts
    context['lfg_upper_count'] = context['lfg_upper'].count()
    context['lfg_lower_count'] = context['lfg_lower'].count()
    
    return render(request, 'lfg/dashboard.html', context)


@login_required
@user_passes_test(profile_activatable, login_url='/lfg/', redirect_field_name=None)
@transaction.atomic
def activate_profile(request):
    """
    View to activate an LFG profile 
    """

    # Check LFG status
    contest = cache.get_or_set(
        'contest_model', Contest.objects.first(), CACHE_TIMEOUT)
    
    if not contest or not contest.lfg_active:
        messages.error(request, 'The LFG service is currently offline.', fail_silently=True)
        return redirect('lfg_dashboard')

    # Update user
    request.user.lfgprofile.active = True
    request.user.lfgprofile.save()

    messages.success(request, 'Profile scheduled for activation.', fail_silently=True)
    
    return redirect('lfg_dashboard')


@login_required
@user_passes_test(new_lfg_user, login_url='/lfg/', redirect_field_name=None)
@transaction.atomic
def create_profile(request):
    """
    View to create an LFG profile.
    """
    
    context = {}

    # Check LFG status
    contest = cache.get_or_set(
        'contest_model', Contest.objects.first(), CACHE_TIMEOUT)
    
    if not contest or not contest.lfg_active:
        messages.error(request, 'The LFG service is currently offline.', fail_silently=True)
        return redirect('lfg_dashboard')

    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST)
        
        if profile_form.is_valid():
            # Create the profile
            lfg_profile = profile_form.save(commit=False)
            lfg_profile.completed = lfg_profile.is_completed()
            lfg_profile.user=request.user
            lfg_profile.save()

            messages.success(request, 'Your profile was created.', fail_silently=True)

            return redirect('lfg_dashboard')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        profile_form = forms.ProfileForm()

    context['profile_form'] = profile_form

    return render(request, 'lfg/profile_form.html', context)


@login_required
@user_passes_test(lfg_profile_active, login_url='/lfg/', redirect_field_name=None)
@transaction.atomic
def deactivate_profile(request):
    """
    View to deactivate an LFG profile.
    """

    # Check LFG status
    contest = cache.get_or_set(
        'contest_model', Contest.objects.first(), CACHE_TIMEOUT)
    
    if not contest or not contest.lfg_active:
        messages.error(request, 'The LFG service is currently offline.', fail_silently=True)
        return redirect('lfg_dashboard')

    # Deactivate profile
    request.user.lfgprofile.active = False
    request.user.lfgprofile.save()

    messages.warning(request, 'Profile scheduled for deactivation.', fail_silently=True)

    return redirect('lfg_dashboard')


@login_required
@user_passes_test(current_lfg_user, login_url='/lfg/', redirect_field_name=None)
@transaction.atomic
def manage_profile(request):
    """
    View to manage an LFG profile.
    """

    context = {}

    # Check LFG status
    contest = cache.get_or_set(
        'contest_model', Contest.objects.first(), CACHE_TIMEOUT)
    
    if not contest or not contest.lfg_active:
        messages.error(request, 'The LFG service is currently offline.', fail_silently=True)
        return redirect('lfg_dashboard')

    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST, instance=request.user.lfgprofile)

        if profile_form.is_valid():
            lfg_profile = profile_form.save(commit=False)

            # Discord username change: profile must be reverified and reactivated
            if 'discord_username' in profile_form.changed_data or 'discord_discriminator' in profile_form.changed_data:
                if lfg_profile.verified:
                    lfg_profile.verified = False
                if lfg_profile.active:
                    lfg_profile.active = False

                messages.warning(request, 'Discord username changed. Profile reverification required.', fail_silently=True)
            # Discord username unchanged
            else:
                # Division was updated 
                if 'division' in profile_form.changed_data:
                    if lfg_profile.active: 
                        if profile_form.cleaned_data['division'] is not None:
                            pass
                        else:
                            lfg_profile.active = False
                            
                            messages.warning(request, 'Profile deactivated because it is incomplete. Complete the blank field(s)  to reactivate.', fail_silently=True)
                # Standing was updated
                elif 'standing' in profile_form.changed_data and lfg_profile.active:
                    if profile_form.cleaned_data['standing'] is None:
                        messages.warning(request, 'Profile deactivated because it is incomplete. Complete the blank field(s)  to reactivate.', fail_silently=True)

            lfg_profile.completed = lfg_profile.is_completed()
            lfg_profile.save()
            
            return redirect('lfg_dashboard')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        profile_form = forms.ProfileForm(instance=request.user.lfgprofile)

    context['profile_form'] = profile_form

    return render(request, 'lfg/profile_form.html', context)
