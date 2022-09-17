from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class Announcement(models.Model):

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
        ordering = ['-updated_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("announcement_detail", kwargs={"slug": str(self.slug)})