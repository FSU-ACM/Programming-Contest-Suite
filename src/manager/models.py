from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListTextField

from register.models import Team

# Create your models here.

class Faculty(models.Model):
    """
    Faculty Model
    - Email address used as primary key due to guaranteed uniqueness
    - Imported by contest organizers before registration opens 
    """

    email = models.EmailField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
        
    def __str__(self):
        return (str(self.first_name) + ' ' + str(self.last_name))


class Course(models.Model):
    """
    Course Model
    - Courses added manually at the this point in time
    - code = 'COP3014'
    - sections = [1, 2, 3, 4, 5]
    """

    code = models.CharField(max_length=8, blank=False)
    sections = ListTextField(base_field=models.IntegerField(), size=10, blank=False)
    instructor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return (str(self.code) + ' ' + str(self.sections))


class Profile(models.Model):
    """
    Profile Model
    - Extends built-in User model
    - team attaches user to a contest team, if null user listed as 'unnamed team' in contest 
    - team_admin gives user ability to delete team, permission transferrable to other teammate
    - fsu_id used for tracking extra credit participation
    - fsu_num used for swipe checkin
    - courses used for extra credit tracking
    - checked_in used to ensure only active participants get extra credit
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    team_admin = models.BooleanField(default=False)
    fsu_id = models.CharField(max_length=8, unique=True, blank=True, null=True)
    fsu_num = models.CharField(max_length=8, unique=True, blank=True, null=True)
    courses = models.ManyToManyField(Course, blank=True)
    checked_in = models.BooleanField(default=False)
    
    def __str__(self):
        return (str(self.user.first_name) + ' ' + str(self.user.last_name))