from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from repository import views as repo_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('signup/', repo_views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='repository/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard and GitHub Config
    path('', repo_views.dashboard_view, name='dashboard'),
    path('github-config/', repo_views.github_config_view, name='github_config'),
    
    # Repository management
    path('repository-choice/', repo_views.repository_choice_view, name='repository_choice'),
    path('new-repository/', repo_views.new_repository_view, name='new_repository'),
    path('existing-repository/', repo_views.existing_repository_view, name='existing_repository'),
    path('repository/<int:repo_id>/', repo_views.repository_detail_view, name='repository_detail'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 