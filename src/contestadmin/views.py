import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render
from django.views import View

from io import BytesIO
from zipfile import ZipFile

from . import forms
from . import tasks
from .utils import contestadmin_auth, ContestAdminAuthMixin
from contestadmin.models import Contest
from contestsuite.settings import MEDIA_ROOT
from lfg.models import LFGProfile
from manager.models import Course, Faculty, Profile
from register.models import Team

# Create your views here.

class DownloadExtraCreditFiles(View):
    """
    View which aggregates all contest participation files into a single ZIP file which is served for download.
    """

    def get(self, request):
        in_memory = BytesIO()
        zip = ZipFile(in_memory, "a")
        
        fpath = MEDIA_ROOT + '/ec_files/'
        for fname in os.listdir(fpath):
            zip.write(fpath+fname, fname)

        # fix for Linux zip files read in Windows
        for file in zip.filelist:
            file.create_system = 0 

        zip.close()

        response = HttpResponse(content_type="application/zip")
        response['Content-Disposition'] = "attachment; filename=all_ec_files.zip"
        
        in_memory.seek(0)    
        response.write(in_memory.read())
        
        return response


class DownloadTSVFiles(View):
    """
    View which aggregates all DOMjudge input files into a single ZIP file which is served for download.
    """

    def get(self, request):
        in_memory = BytesIO()
        zip = ZipFile(in_memory, "a")
        
        fpath = MEDIA_ROOT + '/contest_files/'
        for fname in os.listdir(fpath):
            zip.write(fpath+fname, fname)

        # fix for Linux zip files read in Windows
        for file in zip.filelist:
            file.create_system = 0 

        zip.close()

        response = HttpResponse(content_type="application/zip")
        response['Content-Disposition'] = "attachment; filename=dj_tsv_files.zip"
        
        in_memory.seek(0)    
        response.write(in_memory.read())
        
        return response


class EmailFaculty(View):
    """
    View which schedules a Celery task to email faculty of participation file availability.
    """

    def get(self, request):
        tasks.email_faculty.delay(request.META['HTTP_HOST'])
        messages.info(request, 'Email faculty task scheduled.', fail_silently=True)

        return redirect('admin_dashboard')


class FacultyDashboard(View):
    """
    Views for the faculty dashboard.
    """

    def get(self, request, uidb64):
        """
        View which displays the faculty dashboard.

        uidb64(str): encoding of unique portion of faculty email address
        """

        try:
            faculty_member = Faculty.objects.get(email__contains=force_str(urlsafe_base64_decode(uidb64)))
        except: #(TypeError, ValueError, OverflowError):
            faculty_member = None

        if faculty_member is not None:
            context = {}
            context['courses'] = Course.objects.filter(instructor=faculty_member)
            context['first_name'] = faculty_member.first_name
            context['last_name'] = faculty_member.last_name
            context['uid'] = uidb64
            context['ec_files_available'] = False

            fpath = MEDIA_ROOT + '/ec_files/'
            faculty_id = faculty_member.email.split('@')[0]
            # Determine existance of participation file(s) attached to a faculty mbr
            for fname in os.listdir(fpath):
                if faculty_id in fname:
                    context['ec_files_available'] = True
                    break

            return render(request,'contestadmin/faculty_dashboard.html', context)
        else:
            return HttpResponse('Unable to access faculty dashboard. Please try again later or contact the ACM team.')
    
    def download(self, uidb64):
        """
        View which aggregates all relevant participation files into a single ZIP file which is served for download.

        uidb64(str): encoding of unique portion of faculty email address
        """
        
        try:
            faculty_member = force_str(urlsafe_base64_decode(uidb64))
        except: #(TypeError, ValueError, OverflowError):
            faculty_member = None

        if faculty_member is not None:
            in_memory = BytesIO()
            zip = ZipFile(in_memory, 'a')

            fpath = MEDIA_ROOT + '/ec_files/'
            for fname in os.listdir(fpath):
                # Only append participation files for a given faculty mbr
                if faculty_member in fname:
                    zip.write(fpath+fname, fname)

            # fix for Linux zip files read in Windows
            for file in zip.filelist:
                file.create_system = 0

            zip.close()
            
            response = HttpResponse(content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename=' + faculty_member + '_ec_files.zip'

            in_memory.seek(0)
            response.write(in_memory.read())

            return response
        else:
            return HttpResponse('Unable to serve extra credit files. Please try again later or contact the ACM team.')


class GenerateDomJudgeTSV(View):
    """
    View which schedules a Celery task to generate DOMjudge input files
    """

    def get(self, request):
        tasks.generate_contest_files.delay()
        messages.info(request, 'Generate Contest TSVs task scheduled. Refresh page in a few seconds use download link.', fail_silently=True)

        return redirect('admin_dashboard')


class GenerateExtraCreditReports(View):
    """
    View which schedules a Celery task to generate contest participation files.
    """

    def get(self, request):
        tasks.generate_ec_reports.delay()
        messages.info(request, 'Generate extra credit reports task scheduled. Refresh page in a few seconds use download and email links.', fail_silently=True)

        return redirect('admin_dashboard')


class ExportTeamData(LoginRequiredMixin, ContestAdminAuthMixin, View):
    """
    View which creates and serves a zip file containing contest team data per division.
    """

    def get(self, request):
        """
        Schedules generation of CSV files.
        """

        tasks.generate_team_csvs.delay()
        messages.info(request, 'Team data CSVs generation scheduled.', fail_silently=True)

        return redirect('admin_dashboard')

    def download(self):
        """
        Serves a ZIP file containing all team data CSV files. 
        """
        
        fpath = f"{MEDIA_ROOT}/team_files/"

        # Initialize zip file
        in_memory = BytesIO()
        zip = ZipFile(in_memory, 'a')

        # Add team csvs to zip file
        for fname in os.listdir(fpath):
            zip.write(fpath+fname, fname)

        # fix for Linux zip files read in Windows
        for file in zip.filelist:
            file.create_system = 0 

        zip.close()

        # Initialize response
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=team_data_csvs.zip'
        
        # Write zip file to response
        in_memory.seek(0)    
        response.write(in_memory.read())
        
        return response
    

@login_required
@user_passes_test(contestadmin_auth, login_url='/', redirect_field_name=None)
@transaction.atomic
def dashboard(request):
    """
    View which displays the contst administration dashboard.
    """
    
    context = {}

    if request.method == 'POST':
        # Populate forms with submitted data
        walkin_form = forms.GenerateWalkinForm(request.POST)
        file_form = forms.ResultsForm(request.POST, request.FILES)
        checkin_form = forms.CheckinUsersForm(request.POST)
        update_password_form = forms.UpdatePasswordForm(request.POST)
        profile_role_form = forms.UpdateProfileRoleForm(request.POST)
        account_status_form = forms.AccountStatusForm(request.POST)
        faculty_team_form = forms.DesignateFacultyTeamForm(request.POST)

        # Process walk-in team creation form
        if walkin_form.is_valid():
            tasks.create_walkin_teams.delay(int(walkin_form.cleaned_data['division']), int(walkin_form.cleaned_data['total']))  
            messages.info(request, 'Create teams task scheduled.', fail_silently=True)
        # Process admin check-in form
        elif checkin_form.is_valid():
            tasks.check_in_out_users.delay(
                int(checkin_form.cleaned_data['action']))
            messages.info(request, 'Check in/out task scheduled.',
                          fail_silently=True)
        # Process password update form
        elif update_password_form.is_valid():
            try:
                user = User.objects.get(username=update_password_form.cleaned_data['username'])
            except:
                messages.error(request, 'User not found.', fail_silently=True)
            else:
                try:
                    validate_password(update_password_form.cleaned_data['password'], user)
                except:
                    messages.error(request, 'Please try a different password.', fail_silently=True)
                else:
                    try:
                        user.set_password(update_password_form.cleaned_data['password'])
                        user.save()
                    except:
                        messages.error(request, 'Password save failed.', fail_silently=True)
                    else:
                        messages.success(request, 'Password updated.', fail_silently=True)
        # Process profile role change form
        elif profile_role_form.is_valid():
            try:
                profile = Profile.objects.get(
                    user__username=profile_role_form.cleaned_data['username'])
                # Update role
                profile.role = profile_role_form.cleaned_data['role']
                profile.save()
            except:
                messages.error(request, 'User role update failed.',
                               fail_silently=True)
            else:
                messages.success(request, 'Updated user role.',
                                 fail_silently=True)
        # Process account status update form
        elif account_status_form.is_valid():
            try:
                account = User.objects.get(
                    username=account_status_form.cleaned_data['username'])
            except:
                messages.error(
                    request, 'Unable to locate username in database.', fail_silently=True)
            else:
                if account_status_form.cleaned_data['status'] == '0':
                    # Activate account
                    account.is_active = True
                    account.profile.email_confirmed = True
                elif account_status_form.cleaned_data['status'] == '1':
                    # Deactivate account
                    account.is_active = False
                
                try:
                    account.save()
                except:
                    messages.error(
                        request, 'Account status update failed.', fail_silently=True)
                else:
                    if account_status_form.cleaned_data['status'] == '0':
                        messages.success(
                            request, 'Activated user account.', fail_silently=True)
                    elif account_status_form.cleaned_data['status'] == '1':
                        messages.success(
                            request, 'Deactivated user account.', fail_silently=True)   
        # Process faculty team designation form
        elif faculty_team_form.is_valid():
            try:
                team = Team.objects.get(
                    name=faculty_team_form.cleaned_data['teamname'])
                # Assign faculty team status
                team.faculty = True
                team.save()
            except:
                messages.error(
                    request, 'Faculty team assignment failed.', fail_silently=True)
            else:
                messages.success(
                    request, 'Assigned team faculty status.', fail_silently=True)
        # Process contest results file upload form
        elif file_form.is_valid():
            if Contest.objects.all().count() == 0:
                file_form.save()
                tasks.process_contest_results.delay()
                messages.success(
                        request, 'Results uploaded.', fail_silently=True)
            else:
                try:
                    contest = Contest.objects.all().first()
                except:
                    messages.error(
                        request, 'Failed to upload results. Please try again.', fail_silently=True)
                else:
                    #messages.success(
                    #    request, str(file_form.cleaned_data['results']), fail_silently=True)

                    # Attach results to contest object
                    contest.results = request.FILES['results']
                    contest.save()
                    tasks.process_contest_results.delay()
                    messages.success(
                        request, 'Results uploaded.', fail_silently=True)

        return redirect('admin_dashboard')
    else:
        walkin_form = forms.GenerateWalkinForm()
        file_form = forms.ResultsForm()
        checkin_form = forms.CheckinUsersForm()
        update_password_form = forms.UpdatePasswordForm()
        profile_role_form = forms.UpdateProfileRoleForm()
        account_status_form = forms.AccountStatusForm()
        faculty_team_form = forms.DesignateFacultyTeamForm()
        
    
    # Determine if results files have been uploaded
    if len(os.listdir(MEDIA_ROOT + '/uploads/')) > 0:
        context['dj_results_processed'] = True
    else:
        context['dj_results_processed'] = False

    # Determine if participation reports have been generated
    if len(os.listdir(MEDIA_ROOT + '/ec_files/')) > 0:
        context['ec_files_available'] = True
    else:
        context['ec_files_available'] = False

    # Determine if DOMjudge input files have been generated
    if len(os.listdir(MEDIA_ROOT + '/contest_files/')) > 0:
        context['dj_files_available'] = True
    else:
        context['dj_files_available'] = False

    # Determine if team CSVs have been generated
    context['team_csvs_available'] = True if len(os.listdir(f"{MEDIA_ROOT}/team_files/")) > 0 else False
    
    # Volunteer card data
    context['volunteers'] = [user for user in Profile.objects.order_by('role').all() if user.is_volunteer()]

    # Forms
    context['checkin_form'] = checkin_form
    context['file_form'] = file_form
    context['gen_walkin_form'] = walkin_form
    context['update_password_form'] = update_password_form
    context['profile_role_form'] = profile_role_form
    context['account_status_form'] = account_status_form
    context["faculty_team_form"] = faculty_team_form

    return render(request, 'contestadmin/dashboard.html', context)


@login_required
@user_passes_test(contestadmin_auth, login_url='/', redirect_field_name=None)
def contest_statistics(request):
    """
    View which displays the contest statistics page.
    """
    
    context = {}

    # Users card data
    context['users_registered'] = User.objects.all().count()
    context['users_verified'] = User.objects.filter(is_active=True).count()
    context['users_checkedin'] = Profile.objects.filter(
        checked_in=True).count()
    context['added_fsu_num'] = Profile.objects.exclude(fsu_num=None).count()
    context['added_fsu_id'] = Profile.objects.exclude(fsu_id=None).count()
    context['added_courses'] = Profile.objects.exclude(courses=None).count()

    # Teams card data
    context['total_teams'] = Team.objects.all().count()
    context['registered_teams'] = Team.objects.exclude(
        name__contains='Walk-in-').count()
    context['active_teams'] = [team.is_active() for team in Team.objects.exclude(
        name__contains='Walk-in-')].count(True)
    context['total_walkin'] = Team.objects.filter(
        name__contains='Walk-in-').count()
    context['walkin_used'] = Team.objects.filter(
        name__contains='Walk-in-').exclude(num_members=0).count()

    # Teams Upper division card data
    context['num_upper_teams'] = Team.objects.filter(
        division=1).exclude(name__contains='Walk-in-').count()
    context['num_upper_active_teams'] = [team.is_active() for team in Team.objects.filter(
        division=1).exclude(name__contains='Walk-in-')].count(True)
    context['num_upper_reg_participants'] = Profile.objects.filter(
        team__division=1).exclude(team__name__contains='Walk-in-').count()
    context['num_upper_reg_checkedin_participants'] = Profile.objects.filter(
        team__division=1).filter(checked_in=True).exclude(team__name__contains='Walk-in-').count()
    context['num_upper_walkin_teams'] = Team.objects.filter(
        division=1).filter(name__contains='Walk-in-').count()
    context['num_upper_walkin_used'] = Team.objects.filter(division=1).filter(
        name__contains='Walk-in-').exclude(num_members=0).count()
    context['num_upper_walkin_participants'] = Profile.objects.filter(
        team__division=1).filter(team__name__contains='Walk-in-').count()

    # Teams Lower division card data
    context['num_lower_teams'] = Team.objects.filter(
        division=2).exclude(name__contains='Walk-in-').count()
    context['num_lower_active_teams'] = [team.is_active() for team in Team.objects.filter(
        division=2).exclude(name__contains='Walk-in-')].count(True)
    context['num_lower_reg_participants'] = Profile.objects.filter(
        team__division=2).exclude(team__name__contains='Walk-in-').count()
    context['num_lower_reg_checkedin_participants'] = Profile.objects.filter(
        team__division=2).filter(checked_in=True).exclude(team__name__contains='Walk-in-').count()
    context['num_lower_walkin_teams'] = Team.objects.filter(
        division=2).filter(name__contains='Walk-in-').count()
    context['num_lower_walkin_used'] = Team.objects.filter(division=2).filter(
        name__contains='Walk-in-').exclude(num_members=0).count()
    context['num_lower_walkin_participants'] = Profile.objects.filter(
        team__division=2).filter(team__name__contains='Walk-in-').count()

    # LFG Overview card data
    context['num_lfg_profiles'] = LFGProfile.objects.count()
    context['num_lfg_profiles_incomplete'] = LFGProfile.objects.filter(
        completed=False).count()
    context['num_lfg_profiles_unverified'] = LFGProfile.objects.filter(
        completed=True).filter(verified=False).count()
    context['num_lfg_profiles_inactive'] = LFGProfile.objects.filter(
        completed=True).filter(verified=True).filter(active=False).count()
    context['num_lfg_profiles_active'] = LFGProfile.objects.filter(
        active=True).count()

    # LFG Divisions card data
    context['num_upper_lfg_profiles'] = LFGProfile.objects.filter(
        division=1).count()
    context['num_upper_lfg_profiles_active'] = LFGProfile.objects.filter(
        division=1).filter(active=True).count()
    context['num_lower_lfg_profiles'] = LFGProfile.objects.filter(
        division=2).count()
    context['num_lower_lfg_profiles_active'] = LFGProfile.objects.filter(
        division=2).filter(active=True).count()

    # Course card data
    context['courses'] = Course.objects.all()

    return render(request, 'contestadmin/statistics_dashboard.html', context)