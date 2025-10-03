from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from announcements import models


class LatestAnnouncementsFeed(Feed):
    """
    Simple Django RSS feed of published contest announcements. 
    https://docs.djangoproject.com/en/4.2/ref/contrib/syndication/
    """
    
    title = "ACM at FSU Programming Contest Announcements"
    link = "/announcements/"
    description = "Latest announcments from The Programming Contest Team."

    def items(self):
        return models.Announcement.objects.filter(status=1)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)
