import datetime

import requests as req
from django.core.cache import cache
from django.utils import timezone
from django.views.generic.base import TemplateView

from announcements.models import Announcement
from contestadmin.models import Contest
from contestsuite.settings import CACHE_TIMEOUT, DOMJUDGE_URL
from core.models import Sponsor
from lfg.models import LFGProfile
from manager.models import Course, Profile
from register.models import Team


def _contest_datetime_iso(contest, contest_time):
    if not contest or not contest.contest_date or not contest_time:
        return None

    contest_datetime = datetime.datetime.combine(contest.contest_date, contest_time)
    aware_datetime = timezone.make_aware(
        contest_datetime,
        timezone.get_current_timezone()
    )
    return aware_datetime.isoformat()


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
        context['contest_start_iso'] = _contest_datetime_iso(
            context['contest'],
            context['contest'].contest_start if context['contest'] else None
        )
        context['contest_end_iso'] = _contest_datetime_iso(
            context['contest'],
            context['contest'].contest_end if context['contest'] else None
        )
        
        # Get published announcements
        context['announcements'] = (Announcement.objects.filter(status=1))
        context['sponsors'] = Sponsor.objects.all().extra(select={'ranking_null': 'ranking IS NULL'}).order_by('ranking_null', 'ranking', 'name')

        # Get all courses
        context['courses'] = Course.objects.all()

        if context['contest'] and context['contest'].lfg_active:
            # Get Looking For Group profile totals
            context['lfg_profiles_upper'] = LFGProfile.objects.filter(active=True).filter(division=1).count()
            context['lfg_profiles_lower'] = LFGProfile.objects.filter(active=True).filter(division=2).count()

        ### Teams ###

        teams_set = Team.objects.all()
        participants_set = Profile.objects.all()

        # instead of sorting by a division, now we will sort by faculty=False
        student_teams_set = teams_set.filter(faculty=False).exclude(num_members=0)
        context['num_student_teams'] = student_teams_set.count()
        context['num_student_participants'] = participants_set.filter(
            team__faculty=False).count()

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

        # Sort by faculty=False to get all student teams regardless of Div
        student_teams_set = teams_set.filter(faculty=False).exclude(num_members=0)
        context['student_teams'] = student_teams_set.order_by('-questions_answered', 'score', 'last_submission', 'name')
        context['num_student_teams'] = student_teams_set.count()
        context['num_student_participants'] = participants_set.filter(team__faculty=False).count()

        # Aggregate faculty team and participant info
        faculty_teams_set = teams_set.filter(faculty=True).exclude(num_members=0)
        context['faculty_teams'] = faculty_teams_set.order_by('-questions_answered', 'score', 'last_submission', 'name')
        context['num_faculty_teams'] = faculty_teams_set.count()
        context['num_faculty_participants'] = participants_set.filter(team__faculty=True).count()

        return context


class SponsorsTemplateView(TemplateView):
    """
    View to display sponsors page.
    """

    template_name = 'core/sponsors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all().extra(select={'ranking_null': 'ranking IS NULL'}).order_by('ranking_null', 'ranking', 'name')
        return context
