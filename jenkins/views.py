from django.shortcuts import render

# Create your views here.

def jenkins_dashboard(request):
    return render(request, 'jenkins/jenkins_dashboard.html')