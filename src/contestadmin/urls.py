from django.urls import path

from contestadmin import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('dj_tsv/download', views.DownloadTSVFiles.as_view(), name='download_dj_files'),
    path('ec_files/download', views.DownloadExtraCreditFiles.as_view(), name='download_ec_files'),
    path('ec_files/email_faculty', views.EmailFaculty.as_view(), name='email_faculty'),
    path('ec_files/generate', views.GenerateExtraCreditReports.as_view(), name='gen_ec_reports'),
    path('faculty/<uidb64>/', views.FacultyDashboard.as_view(), name='fac_ec_dashboard'),
    path('faculty/<uidb64>/download', views.FacultyDashboard.download, name='fac_ec_files_dl'),
    path('statistics/', views.contest_statistics, name='contest_stats'),
    path('team_csvs/generate', views.ExportTeamData.as_view(), name='generate_team_csvs'),
    path('team_csvs/download', views.ExportTeamData.download, name='download_team_csvs')
]
