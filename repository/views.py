import os
import json
import shutil
import hashlib
import subprocess
import requests
from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .forms import (
    SignUpForm, GitHubConfigForm, NewRepositoryForm, 
    ExistingRepositoryForm, FileUploadForm, FolderUploadForm
)
from .models import GitHubConfig, Repository


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'repository/signup.html', {'form': form})


@login_required
def dashboard_view(request):
    try:
        github_config = GitHubConfig.objects.get(user=request.user)
        has_github_config = True
    except GitHubConfig.DoesNotExist:
        has_github_config = False
        
    repositories = Repository.objects.filter(user=request.user)
    
    return render(request, 'repository/dashboard.html', {
        'has_github_config': has_github_config,
        'repositories': repositories
    })


@login_required
def github_config_view(request):
    try:
        github_config = GitHubConfig.objects.get(user=request.user)
    except GitHubConfig.DoesNotExist:
        github_config = None
    
    if request.method == 'POST':
        form = GitHubConfigForm(request.POST, instance=github_config)
        if form.is_valid():
            config = form.save(commit=False)
            config.user = request.user
            config.noreply_email = f"{config.github_username}@users.noreply.github.com"
            config.save()
            return redirect('dashboard')
    else:
        form = GitHubConfigForm(instance=github_config)
        
    return render(request, 'repository/github_config.html', {'form': form})


@login_required
def repository_choice_view(request):
    return render(request, 'repository/repository_choice.html')


@login_required
def new_repository_view(request):
    if request.method == 'POST':
        form = NewRepositoryForm(request.POST)
        if form.is_valid():
            # Get GitHub config
            try:
                github_config = GitHubConfig.objects.get(user=request.user)
            except GitHubConfig.DoesNotExist:
                return redirect('github_config')
            
            # Create repository via GitHub API
            repo_name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            is_private = form.cleaned_data['is_private']
            
            headers = {"Authorization": f"token {github_config.github_token}"}
            data = {
                "name": repo_name,
                "description": description,
                "private": is_private,
                "auto_init": False
            }
            
            response = requests.post(
                "https://api.github.com/user/repos", 
                json=data, 
                headers=headers
            )
            
            if response.status_code != 201:
                error_msg = f"Repository creation failed: {response.status_code} {response.text}"
                return render(request, 'repository/new_repository.html', {
                    'form': form,
                    'error': error_msg
                })
                
            # Create local repository
            repo_dir = os.path.join(settings.MEDIA_ROOT, request.user.username, repo_name)
            os.makedirs(repo_dir, exist_ok=True)
            
            # Initialize git repository
            repo_url = f"https://{github_config.github_token}@github.com/{github_config.github_username}/{repo_name}.git"
            
            subprocess.run(["git", "init"], cwd=repo_dir)
            subprocess.run(["git", "config", "user.name", github_config.github_username], cwd=repo_dir)
            subprocess.run(["git", "config", "user.email", github_config.noreply_email], cwd=repo_dir)
            subprocess.run(["git", "checkout", "-b", "main"], cwd=repo_dir)
            
            # Create GitHub Actions workflow
            workflows_dir = os.path.join(repo_dir, ".github", "workflows")
            os.makedirs(workflows_dir, exist_ok=True)
            
            with open(os.path.join(workflows_dir, "main.yml"), "w") as wf:
                wf.write("""
name: AutoRun on Upload

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Show uploaded files
        run: ls -la
      - name: Say Hello
        run: echo "🚀 GitHub Action triggered successfully!"
""".strip())
            
            # Create README.md
            with open(os.path.join(repo_dir, "README.md"), "w") as f:
                f.write(f"# {repo_name}\n{description}")
            
            # Initial commit and push
            subprocess.run(["git", "add", "."], cwd=repo_dir)
            subprocess.run(["git", "commit", "-m", "Initial commit with GitHub Actions"], cwd=repo_dir)
            subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=repo_dir)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_dir)
            
            # Save repository to database
            repository = form.save(commit=False)
            repository.user = request.user
            repository.url = f"https://github.com/{github_config.github_username}/{repo_name}"
            repository.local_path = repo_dir
            repository.save()
            
            return redirect('repository_detail', repo_id=repository.id)
    else:
        form = NewRepositoryForm()
        
    return render(request, 'repository/new_repository.html', {'form': form})


@login_required
def existing_repository_view(request):
    if request.method == 'POST':
        form = ExistingRepositoryForm(request.POST)
        if form.is_valid():
            # Get GitHub config
            try:
                github_config = GitHubConfig.objects.get(user=request.user)
            except GitHubConfig.DoesNotExist:
                return redirect('github_config')
            
            repo_name = form.cleaned_data['name']
            
            # Create local repository directory
            repo_dir = os.path.join(settings.MEDIA_ROOT, request.user.username, repo_name)
            os.makedirs(repo_dir, exist_ok=True)
            
            # Initialize git repository and connect to remote
            repo_url = f"https://{github_config.github_token}@github.com/{github_config.github_username}/{repo_name}.git"
            
            subprocess.run(["git", "init"], cwd=repo_dir)
            subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=repo_dir)
            subprocess.run(["git", "fetch"], cwd=repo_dir)
            subprocess.run(["git", "checkout", "main"], cwd=repo_dir)
            
            # Save repository to database
            repository = Repository(
                user=request.user,
                name=repo_name,
                url=f"https://github.com/{github_config.github_username}/{repo_name}",
                local_path=repo_dir
            )
            repository.save()
            
            return redirect('repository_detail', repo_id=repository.id)
    else:
        form = ExistingRepositoryForm()
        
    return render(request, 'repository/existing_repository.html', {'form': form})


@login_required
def repository_detail_view(request, repo_id):
    repository = get_object_or_404(Repository, id=repo_id, user=request.user)
    file_form = FileUploadForm()
    folder_form = FolderUploadForm()
    
    if request.method == 'POST':
        if 'file' in request.FILES:
            file_form = FileUploadForm(request.POST, request.FILES)
            if file_form.is_valid():
                uploaded_file = request.FILES['file']
                file_path = os.path.join(repository.local_path, uploaded_file.name)
                
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                        
                # Git operations
                subprocess.run(["git", "add", "."], cwd=repository.local_path)
                subprocess.run(["git", "commit", "-m", f"Upload: {uploaded_file.name}"], cwd=repository.local_path)
                subprocess.run(["git", "push", "origin", "main"], cwd=repository.local_path)
                
                return redirect('repository_detail', repo_id=repository.id)
                
        elif 'folder' in request.FILES:
            folder_form = FolderUploadForm(request.POST, request.FILES)
            if folder_form.is_valid():
                files = request.FILES.getlist('folder')
                uploaded_files = []
                
                for f in files:
                    if f and f.name:
                        file_path = os.path.join(repository.local_path, f.name)
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        
                        with open(file_path, 'wb+') as destination:
                            for chunk in f.chunks():
                                destination.write(chunk)
                                
                        uploaded_files.append(f.name)
                
                # Git operations if files were uploaded
                if uploaded_files:
                    subprocess.run(["git", "add", "."], cwd=repository.local_path)
                    commit_msg = "Upload: " + ", ".join(uploaded_files[:5])
                    if len(uploaded_files) > 5:
                        commit_msg += f" and {len(uploaded_files) - 5} more files"
                    subprocess.run(["git", "commit", "-m", commit_msg], cwd=repository.local_path)
                    subprocess.run(["git", "push", "origin", "main"], cwd=repository.local_path)
                
                return redirect('repository_detail', repo_id=repository.id)
    
    # List files in the repository
    try:
        files = os.listdir(repository.local_path)
        # Filter out .git directory
        files = [f for f in files if f != '.git']
    except Exception as e:
        files = []
        error = str(e)
    
    return render(request, 'repository/repository_detail.html', {
        'repository': repository,
        'file_form': file_form,
        'folder_form': folder_form,
        'files': files
    }) 