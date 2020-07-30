from django.urls import path

from . import views

urlpatterns = [
    # contest suite homepage
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('teams/', views.teams, name='teams'),
]
