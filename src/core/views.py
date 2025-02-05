from django.core.cache import cache
from django.views.generic.base import TemplateView

import requests as req

from announcements.models import Announcement
from contestadmin.models import Contest
from contestsuite.settings import CACHE_TIMEOUT, DOMJUDGE_URL
from register.models import Team
from manager.models import Course, Profile
from lfg.models import LFGProfile

# Create your views here.

class IndexTemplateView(TemplateView):
    """
    View to display site index(home) page. Displays announcements, DOMjudge server status, and information on 
    extra credit courses, participation, teams, and looking for group participants. 
    """

    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Get cached DOMjudge server status or ping server
        if cache.get('domjudge_status'):
            context['domjudge_status'] = cache.get('domjudge_status')
        else:
            try:
                r = req.head(DOMJUDGE_URL, timeout=3)
            except req.ConnectionError:
                context['domjudge_status'] = None
            else:
                context['domjudge_status'] = r.status_code
                cache.set('domjudge_status', r.status_code, CACHE_TIMEOUT)

        # Get contest object or set to None
        context['contest'] = cache.get_or_set(
            'contest_model', Contest.objects.first(), CACHE_TIMEOUT)
        
        # Get published announcements
        context['announcements'] = (Announcement.objects.filter(status=1))
        # Get all courses
        context['courses'] = Course.objects.all()

        if context['contest'] and context['contest'].lfg_active:
            # Get Looking For Group profile totals
            context['lfg_profiles_upper'] = LFGProfile.objects.filter(active=True).filter(division=1).count()
            context['lfg_profiles_lower'] = LFGProfile.objects.filter(active=True).filter(division=2).count()

        ### Teams ###

        teams_set = Team.objects.all()
        participants_set = Profile.objects.all()

        # Aggregate upper division team and participant info
        upper_teams_set = teams_set.filter(division=1).filter(
            faculty=False).exclude(num_members=0)
        context['num_upper_teams'] = upper_teams_set.count()
        context['num_upper_participants'] = participants_set.filter(
            team__division=1).count()

        #  Aggregate lower division team and participant info
        lower_teams_set = teams_set.filter(division=2).filter(
            faculty=False).exclude(num_members=0)
        context['num_lower_teams'] = lower_teams_set.count()
        context['num_lower_participants'] = participants_set.filter(
            team__division=2).count()

        # Aggregate faculty team and participant info
        faculty_teams_set = teams_set.filter(faculty=True).exclude(num_members=0)
        context['num_faculty_teams'] = faculty_teams_set.count()
        context['num_faculty_participants'] = participants_set.filter(
            team__faculty=True).count()
        
        return context


class ContactTemplateView(TemplateView):
    """
    View to display contact us page.
    """

    template_name = 'core/contact.html'


class FaqTemplateView(TemplateView):
    """
    View to display faq page.
    """

    template_name = 'core/faq.html'


class TeamsTemplateView(TemplateView):
    """
    View to display teams page.
    """

    template_name = 'core/teams.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Get contest object or set to None
        context['contest'] = cache.get_or_set(
            'contest_model', Contest.objects.first(), CACHE_TIMEOUT)

        teams_set = Team.objects.all()
        participants_set = Profile.objects.all()

        # Aggregate upper division team and participant info
        upper_teams_set = teams_set.filter(division=1).filter(faculty=False).exclude(num_members=0)
        context['upper_teams'] = upper_teams_set.order_by('-questions_answered', 'score', 'name')
        context['num_upper_teams'] = upper_teams_set.count()
        context['num_upper_participants'] = participants_set.filter(team__division=1).count()

        #  Aggregate lower division team and participant info
        lower_teams_set = teams_set.filter(division=2).filter(faculty=False).exclude(num_members=0)
        context['lower_teams'] = lower_teams_set.order_by('-questions_answered', 'score', 'name')
        context['num_lower_teams'] = lower_teams_set.count()
        context['num_lower_participants'] = participants_set.filter(team__division=2).count()

        # Aggregate faculty team and participant info
        faculty_teams_set = teams_set.filter(faculty=True).exclude(num_members=0)
        context['faculty_teams'] = faculty_teams_set.order_by('-questions_answered', 'score', 'name')
        context['num_faculty_teams'] = faculty_teams_set.count()
        context['num_faculty_participants'] = participants_set.filter(team__faculty=True).count()

        return context
