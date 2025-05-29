from django.urls import path
from . import views

urlpatterns = [
    path('', views.jenkins_dashboard, name='jenkins_dashboard'),
]
