from django.db import models
from django.contrib.auth.models import User


# Create your models here.	

class Team(models.Model):
    """
    Team Model

    DIVISION:
        Upper Division: the team is a member of the Upper Division
        Lower Division: the team is a member of the Lower Division

    name (CharField): the team's name

    division (PositiveSmallIntegerField): the division in which the team will compete with choices defined in Team.DIVISION

    pin (CharField): the alphanumeric code a user must provide to join an existing team

    contest_id (CharField): the team's DOMjudge username

    contest_password (CharField): the team's DOMjudge password

    questions_answered (PositiveSmallIntegerField): the number of contest packet questions the team successfully answered 

    score (PositiveSmallIntegerField): the team's final DOMjudge score

    last_submission (PositiveSmallIntegerField): the team's last submission time

    num_members (PositiveSmallIntegerField): the number of users on the team

    faculty (BooleanField): If True, the team contains at least one faculty member. Otherwise the team does not contain a faculty member.
    """

    DIVISION = (
        (1, 'Upper Division'),
        (2, 'Lower Division')
    )
    
    name = models.CharField(max_length=30, unique=True)
    division = models.PositiveSmallIntegerField(choices=DIVISION)
    pin = models.CharField(max_length=6, unique=True)
    contest_id = models.CharField(max_length=7, unique=True, blank=True, null=True)
    contest_password = models.CharField(max_length=6, unique=True, blank=True, null=True)
    questions_answered = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0)
    last_submission = models.PositiveSmallIntegerField(default=0)
    num_members = models.PositiveSmallIntegerField(default=0)
    faculty = models.BooleanField(default=False)

    def __str__(self):
        return (str(self.name) + ' : ' + ('U' if self.division == 1 else 'L'))

    def get_division(self):
        """
        Returns the team's division name.
        """
        
        if self.faculty:
            division = "Faculty"
        elif self.division == 1:
            division = "Upper"
        else:
            division = "Lower"

        return division
    
    def get_division_code(self):
        """
        Returns the team's division short name.
        """
        
        if self.faculty:
            division = "F"
        elif self.division == 1:
            division = "U"
        else:
            division = "L"

        return division            
    
    def get_members(self):
        """
        Returns a list of team member names.
        """
        
        members = User.objects.filter(profile__team=self)

        member_names = []
        for member in members:
            member_names.append(member.get_full_name())

        return member_names

    def is_active(self):
        """
        Returns whether at least one team member checked into the contest.
        """

        members = User.objects.filter(profile__team=self)

        for member in members:
            if member.profile.checked_in == True:
                return True
        
        return False
