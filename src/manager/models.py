from django.db import models
from django.contrib.auth.models import User

from hashid_field import HashidField

from register.models import Team

# Create your models here.

class Faculty(models.Model):
    """
    Faculty Model

    email (EmailField): the FSU CS email of the faculty member

    first_name (CharField): the first name of the faculty member

    last_name (CHarField): the last name of the faculty member
    """

    email = models.EmailField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return (str(self.first_name) + ' ' + str(self.last_name))
    
    def get_first_initial(self):
        return(self.first_name[0])


class Course(models.Model):
    """
    Course Model

    code (CharField): the FSU code of a course (ex. COP3014)

    name (CharField): the course name (ex. Programming I)
    
    instructor (ForeignKey): the course's istructor
    """

    code = models.CharField(max_length=8)
    name = models.CharField(max_length=50)
    instructor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return (str(self.code) + ' : ' + str(self.name) + ' - ' + str(self.instructor.last_name) + ', ' + str(self.instructor.get_first_initial()))

    def num_checkedin(self):
        """
        Returns the number of users who have added the course to their profile
        and checked into the contest.
        """
        
        return Profile.objects.filter(courses=self).filter(checked_in=True).count()

    def num_registered(self):
        """
        Returns the number of users who have added the course to their profile.
        """
        
        return Profile.objects.filter(courses=self).count()


class Profile(models.Model):
    """
    Profile Model

    ROLES:
        Contestant: a user who is registered to compete in the contest
        Docent: a user who is registered to volunteer as a docent at the contest
        Proctor: a user who is registered to volunteer as a proctor at the contest
        Question Writer: a user who is registered to volunteer to write a contest question
        Organizer: a 

    user (OneToOneField): the base user account which the profile extends

    role (PositiveSmallIntegerField): the profile's role as defined in Profile.ROLES

    team (ForeignKey): the team which the user has joined

    team_admin (BooleanField): whether the user is a team admin 

    fsu_id (CHarField): the user's FSUID used for identification in extra credit files

    fsu_num (HashidField): the last 8 digits of the user's FSU number used for swipe check-in

    courses (ManyToManyField): the extra credit courses in which a user is enrolled

    checked_in (BooleanField): whether the user has checked into the programming contest

    email_confirmed (BooleanField): whether the user's email address has been confirmed

    announcement_email_opt_out (BooleanField): whether the user has opted out of receiving announcement emails
    """

    ROLES = (
        (1, 'Contestant'),
        (2, 'Docent'),
        (3, 'Proctor'),
        (4, 'Question Writer'),
        (5, 'Organizer')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.PositiveSmallIntegerField(choices=ROLES, default=1)
    team = models.ForeignKey(Team, related_name='profile_team', on_delete=models.SET_NULL, blank=True, null=True)
    team_admin = models.BooleanField(default=False)
    fsu_id = models.CharField(max_length=8, unique=True, blank=True, null=True)
    fsu_num = HashidField(blank=True, null=True)
    courses = models.ManyToManyField(Course, blank=True)
    checked_in = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    announcement_email_opt_out = models.BooleanField(default=False)
    
    def __str__(self):
        return (str(self.user.first_name) + ' ' + str(self.user.last_name))

    def get_role(self):
        """
        Returns the profile's role.
        """
        
        return self.ROLES[self.role-1][1]
    
    def has_team(self):
        """
        Returns (bool) whether the profile is attached to a team.
        """
        
        return self.team is not None

    def has_courses(self):
        """
        Returns (bool) whether the profile has selected any extra credit courses.
        """
        
        return self.courses.count() != 0

    def is_volunteer(self):
        """
        Returns (bool) whether the profile has a volunteer role.
        """
        
        return self.role > 1

    def is_organizer(self):
        """
        Returns (bool) whether the profile has the Organizer role.
        """
        
        return self.role == 5
