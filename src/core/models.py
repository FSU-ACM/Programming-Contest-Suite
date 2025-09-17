from django.db import models

# Create your models here.

class Sponsor(models.Model):
    """
    Contest sponsor model. Each model stores the details of a contest sponsor, including
    name, logo, link to sponsor's website, message, and ranking.

    name (CharField): the sponsor name (unique)

    logo (ImageField): the sponsor logo

    url (URLField): the sponsor URL

    message (TextField): the sponsor message
    
    ranking (PositiveIntegerField): the sponsor display ranking (optional, lower numbers appear first)
    """

    name = models.CharField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='sponsors')
    url = models.URLField(blank=True)
    message = models.TextField(blank=True)
    ranking = models.PositiveIntegerField(blank=True, null=True, help_text="Lower numbers appear first. Blank rankings appear last.")

    def __str__(self):
        return self.name