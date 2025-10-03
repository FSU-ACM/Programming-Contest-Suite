from django.urls import path

from announcements import feeds
from announcements import views


urlpatterns = [
    path('', views.AnnouncementListView.as_view(), name='announcements'),
    path("feed/rss", feeds.LatestAnnouncementsFeed(), name="announcements_feed"),
    path('<slug:slug>/', views.AnnouncementDetailView.as_view(), name='announcement_detail'),
]
