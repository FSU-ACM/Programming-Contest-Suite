from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Contest(models.Model):
    """
    Contest Model
    -  Contains all relevate information for a specific programming test

    contest_date (DateField): date of the contest

    contest_doors (TimeField): time at which contestants can begin checking into the contest

    contest_start (TimeField): time at which contestants may start working on the contest question packet

    contest_freeze (TimeField): time at which the DOMjudge scoreboard is frozen

    contest_end (TimeField): deadline to submit question solutions to DOMjudge

    contest_awards (TimeField): time at which the post contest awards ceremony beings

    team_deadline (DateTimeField): deadline for a contestant to create a registered team

    results (FileField): a file containing DOMjudge results 

    ec_processed (bool): If True, contest participation files have been generated; otherwise False.

    volunteer_pin (CharField): the pass code contest volunteers must provide to complete volunteer check-in

    participation (PositiveSmallIntegerField): the contest participation format with choices deinfed in Contest.FORMAT

    lfg_active (BooleanField): If False, the Looking For Group is inacitve. If True, the service is active.

    lunch_form_url (URLField): the URL of the lunch preference survey

    order_tshirt_url (URLField): the URL of the page to order a contest t-shirt
    """

    FORMAT = (
        (1, 'In-Person'),
        (2, 'Virtual'),
        (3, 'Hybrid')
    )

    contest_date = models.DateField(auto_now=False)
    contest_doors = models.TimeField(auto_now=False, blank=True, null=True)
    contest_start = models.TimeField(auto_now=False, blank=True, null=True)
    contest_freeze = models.TimeField(auto_now=False, blank=True, null=True)
    contest_end = models.TimeField(auto_now=False, blank=True, null=True)
    contest_awards = models.TimeField(auto_now=False, blank=True, null=True)
    team_deadline = models.DateTimeField(auto_now=False, blank=True, null=True)
    results = models.FileField(upload_to='uploads/', blank=True)
    ec_processed = models.BooleanField(default=False)
    volunteer_pin = models.CharField(max_length=8, default='thankyou')
    participation = models.PositiveSmallIntegerField(choices=FORMAT, default=1)
    lfg_active = models.BooleanField(default=False)
    lunch_form_url = models.URLField(blank=True, null=True)
    order_tshirt_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return ("Programming Contest on "+str(self.contest_date))

    def get_participation(self):
        """
        Returns the contest participation format.
        """
        
        if self.participation:
            return self.FORMAT[self.participation - 1][1]
        else:
            return 'TBA'
        

    def is_contest_complete(self):
        """
        Returns true if contest is complete, false otherwise
        """
        
        return self.results != "" and self.results is not None
