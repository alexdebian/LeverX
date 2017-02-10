from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Project, User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = {'title', 'description', 'due_date', 'developer'}


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = {'title', 'description', 'managers', 'tasks'}


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2'}


