from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Announcement(models.Model):
    """
    Contest announcement model. Each announcement stores text content displayable on the
    registration site and optionally distributed via Discord and/or email.

    STATUS:
        Draft: announcement is saved in the database and viewable in Django Admin but not displayed in the
            public announcement list nor sent via Discord/email.
        
        Publish: announcement is is saved in the database, viewable in Django Admin, displayed in the
            public announcement, optionally sent via Discord/email.

    title (CharField): the announcement title (unique)
    
    slug (SlugField): announcement text slug (unique)

    author (ForeignKey: User): announcement author

    updated_on (DateTimeField): date and time the announcement was last updated
    
    content (TextField): announcement's content

    created_on (DateTimeField): date and time the announcement was created

    status (IntegerField): the announcement's state with choices defined in Announcement.STATUS 

    send_discord (BooleanField): If False the announcement is not delivered to the Discord endpoint. If True the announcement
        is delivered to the Discord webhook using the URL defined in the ANNOUNCEMENT_WEBHOOK_URL environment variable.

    send_email (BooleanField): If False the announcement is not distributed to users' email. If True the announcement
        is delivered to users whose profile have the announcement_email_opt_out feature set to False.
    """

    STATUS = (
        (0,"Draft"),
        (1,"Publish")
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='contest_announcements')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    send_discord = models.BooleanField(default=True)
    send_email = models.BooleanField(default=True)

    class Meta:
        # Descending order: most -> least recently updated
        ordering = ['-updated_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("announcement_detail", kwargs={"slug": str(self.slug)})
