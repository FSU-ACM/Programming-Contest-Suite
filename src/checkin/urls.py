from django.urls import path

from checkin import views


urlpatterns = [
    path('', views.checkin, name='checkin'),
    path('result/', views.checkin_result, name='checkin_result'),
    path('volunteer/', views.volunteer_checkin, name='volunteer_checkin'),
]
