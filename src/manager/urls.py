from django.urls import path

from manager import views


urlpatterns = [
    path('', views.dashboard, name='manage_dashboard'),
    path('courses/', views.manage_courses, name='manage_courses'),
    path('courses/clear/', views.clear_courses, name='clear_courses'),
    path('profile/', views.manage_profile, name='manage_profile'),
    path('team/', views.manage_team, name='manage_team'),
    path('team/delete/', views.delete_team, name='delete_team'),
    path('team/join/', views.join_team, name='join_team'),
    path('team/leave/', views.leave_team, name='leave_team'),
    path('team/remove/<str:username>', views.remove_member, name='remove_member'),
]
