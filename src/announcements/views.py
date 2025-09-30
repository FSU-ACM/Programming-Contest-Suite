from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from announcements.models import Announcement


class AnnouncementListView(ListView):
    """
    Simple view which lists all announcement objects in the database.
    """

    model = Announcement
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()

        return context

    def get_queryset(self):
        return Announcement.objects.filter(status=1)


class AnnouncementDetailView(DetailView):
    """
    Simple view which lists the details of an announcement object in the database.
    """

    model = Announcement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        
        return context
