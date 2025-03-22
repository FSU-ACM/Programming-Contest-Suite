from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path

from . import views
from .utils import contestadmin_auth

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('dj_tsv/download', login_required((user_passes_test(contestadmin_auth, login_url='/', redirect_field_name=None))(views.DownloadTSVFiles.as_view())), name='download_dj_files'),
    path('dj_tsv/generate', login_required((user_passes_test(contestadmin_auth, login_url='/', redirect_field_name=None))(views.GenerateDomJudgeTSV.as_view())), name='gen_dj_files'),
    path('ec_files/download', login_required((user_passes_test(contestadmin_auth, login_url='/', redirect_field_name=None))(views.DownloadExtraCreditFiles.as_view())), name='download_ec_files'),
    path('ec_files/email_faculty', login_required((user_passes_test(contestadmin_auth, login_url='/', redirect_field_name=None))(views.EmailFaculty.as_view())), name='email_faculty'),
    path('ec_files/generate', login_required((user_passes_test(contestadmin_auth, login_url='/', redirect_field_name=None))(views.GenerateExtraCreditReports.as_view())), name='gen_ec_reports'),
    path('faculty/<uidb64>/', views.FacultyDashboard.as_view(), name='fac_ec_dashboard'),
    path('faculty/<uidb64>/download', views.FacultyDashboard.download, name='fac_ec_files_dl'),
    path('statistics/', views.contest_statistics, name='contest_stats'),
    path('team_csvs/generate', views.ExportTeamData.as_view(), name='generate_team_csvs'),
    path('team_csvs/download', views.ExportTeamData.download, name='download_team_csvs')
]
