import os

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render
from django.views import View

from io import BytesIO
from zipfile import ZipFile

from . import forms
from . import tasks
from .utils import contestadmin_auth
from contestadmin.models import Contest
from contestsuite.settings import MEDIA_ROOT
from manager.models import Course, Faculty, Profile
from register.models import Team

# Create your views here.

class DownloadExtraCreditFiles(View):

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

    def get(self, request):
        tasks.email_faculty.delay(request.META['HTTP_HOST'])
        messages.info(request, 'Email faculty task scheduled.', fail_silently=True)

        return redirect('admin_dashboard')


class FacultyDashboard(View):

    def get(self, request, uidb64):
        try:
            faculty_member = Faculty.objects.get(email__contains=force_text(urlsafe_base64_decode(uidb64)))
        except: #(TypeError, ValueError, OverflowError):
            faculty_member = None

        if faculty_member is not None:
            context = {}
            context['first_name'] = faculty_member.first_name
            context['last_name'] = faculty_member.last_name
            context['uid'] = uidb64

            return render(request,'contestadmin/faculty_dashboard.html', context)
    
    def download(self, uidb64):
        try:
            faculty_member = force_text(urlsafe_base64_decode(uidb64))
        except: #(TypeError, ValueError, OverflowError):
            faculty_member = None

        if faculty_member is not None:
            in_memory = BytesIO()
            zip = ZipFile(in_memory, 'a')

            fpath = MEDIA_ROOT + '/ec_files/'
            for fname in os.listdir(fpath):
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

    def get(self, request):
        tasks.generate_contest_files.delay()
        messages.info(request, 'Generate Contest TSVs task scheduled. Refresh page in a few seconds use download link.', fail_silently=True)

        return redirect('admin_dashboard')


class GenerateExtraCreditReports(View):

    def get(self, request):
        tasks.generate_ec_reports.delay()
        messages.info(request, 'Generate extra credit reports task scheduled. Refresh page in a few seconds use download and email links.', fail_silently=True)

        return redirect('admin_dashboard')


@user_passes_test(contestadmin_auth, login_url='/', redirect_field_name=None)
@transaction.atomic
def dashboard(request):
    context = {}

    if request.method == 'POST':
        walkin_form = forms.GenerateWalkinForm(request.POST)
        file_form = forms.ResultsForm(request.POST, request.FILES)
        checkin_form = forms.CheckinUsersForm(request.POST)
        if walkin_form.is_valid():
            tasks.create_walkin_teams.delay(int(walkin_form.cleaned_data['division']), int(walkin_form.cleaned_data['total']))  
            messages.info(request, 'Create teams task scheduled.', fail_silently=True)
        elif checkin_form.is_valid():
            tasks.check_in_out_users.delay(
                int(checkin_form.cleaned_data['action']))
            messages.info(request, 'Check in/out task scheduled.',
                          fail_silently=True)
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
                    messages.success(
                        request, str(file_form.cleaned_data['results']), fail_silently=True)
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
        
    
    if len(os.listdir(MEDIA_ROOT + '/uploads/')) > 0:
        context['dj_results_processed'] = True
    else:
        context['dj_results_processed'] = False

    if len(os.listdir(MEDIA_ROOT + '/ec_files/')) > 0:
        context['ec_files_available'] = True
    else:
        context['ec_files_available'] = False

    if len(os.listdir(MEDIA_ROOT + '/contest_files/')) > 0:
        context['dj_files_available'] = True
    else:
        context['dj_files_available'] = False
    
    
    # Users card data
    context['users_registered'] = User.objects.all().count()
    context['users_verified'] = User.objects.filter(is_active=True).count()
    context['added_fsu_num'] = Profile.objects.exclude(fsu_num=None).count()
    context['added_fsu_id'] = Profile.objects.exclude(fsu_id=None).count()
    context['added_courses'] = Profile.objects.exclude(courses=None).count()

    # Teams card data
    context['total_teams'] = Team.objects.all().count()
    context['registered_teams'] = Team.objects.exclude(name__contains='Walk-in-').count()
    context['total_walkin'] = Team.objects.filter(name__contains='Walk-in-').count()
    context['walkin_used'] = Team.objects.filter(name__contains='Walk-in-').exclude(num_members=0).count()

    # Upper division card data
    context['num_upper_teams'] = Team.objects.filter(division=1).exclude(name__contains='Walk-in-').count()
    context['num_upper_reg_participants'] = Profile.objects.filter(team__division=1).exclude(team__name__contains='Walk-in-').count()
    context['num_upper_walkin_teams'] = Team.objects.filter(
        division=1).filter(name__contains='Walk-in-').count()
    context['num_upper_walkin_used'] = Team.objects.filter(division=1).filter(
        name__contains='Walk-in-').exclude(num_members=0).count()
    context['num_upper_walkin_participants'] = Profile.objects.filter(team__division=1).filter(team__name__contains='Walk-in-').count()

    # Lower division card data
    context['num_lower_teams'] = Team.objects.filter(division=2).exclude(name__contains='Walk-in-').count()
    context['num_lower_reg_participants'] = Profile.objects.filter(team__division=2).exclude(team__name__contains='Walk-in-').count()
    context['num_lower_walkin_teams'] = Team.objects.filter(
        division=2).filter(name__contains='Walk-in-').count()
    context['num_lower_walkin_used'] = Team.objects.filter(division=2).filter(
        name__contains='Walk-in-').exclude(num_members=0).count()
    context['num_lower_walkin_participants'] = Profile.objects.filter(team__division=2).filter(team__name__contains='Walk-in-').count()

    # Course crard data
    context['courses'] = Course.objects.all()

    # Forms
    context['checkin_form'] = checkin_form
    context['file_form'] = file_form
    context['gen_walkin_form'] = walkin_form

    return render(request, 'contestadmin/dashboard.html', context)
