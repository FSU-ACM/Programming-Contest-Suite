"""
Functions useable by @user_passes_test view decorator
"""

from lfg.models import LFGProfile


def profile_activatable(user):
    try:
        return user.lfgprofile.is_activatable()
    except:
        return False


def new_lfg_user(user):
    try:
        return not LFGProfile.objects.filter(user=user).exists()
    except:
        return False


def current_lfg_user(user):
    try:
        return LFGProfile.objects.filter(user=user).exists()
    except:
        return False


def lfg_profile_active(user):
    try:
        return user.lfgprofile.active
    except:
        return False