from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('contact/', views.ContactTemplateView.as_view(), name='contact'),
    path('faq/', views.FaqTemplateView.as_view(), name='faq'),
    path('teams/', views.TeamsTemplateView.as_view(), name='teams'),
    path('sponsors/', views.SponsorsTemplateView.as_view(), name='sponsors'),
]
