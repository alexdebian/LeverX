from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_complete, password_change
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from .models import Task, Project, User
from .forms import TaskForm, ProjectForm, MyUserCreationForm


# ----------------------------------------------------------------------------------------------------------------------
class HomeView(TemplateView):
    template_name = 'index.html'


def developer_list(request):
    developers = User.objects.filter(role=2)
    return render(request, 'employee/developer_list.html', {'developers': developers})


# ----------------------------------------------------------------------------------------------------------------------
def task_list(request):
    tasks = Task.objects.all()
    projects = Project.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'projects': projects})


def save_task_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            data['form_is_valid'] = True
            tasks = Task.objects.all()
            data['html_task_list'] = render_to_string('tasks/includes/partial_task_list.html', {'tasks': tasks})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
    else:
        form = TaskForm()
    return save_task_form(request, form, 'tasks/includes/partial_task_create.html')


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
    else:
        form = TaskForm(instance=task)
    return save_task_form(request, form, 'tasks/includes/partial_task_update.html')


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = dict()
    if request.method == 'POST':
        task.delete()
        data['form_is_valid'] = True
        tasks = Task.objects.all()
        data['html_task_list'] = render_to_string('tasks/includes/partial_task_list.html', {'tasks': tasks})
    else:
        context = {'task': task}
        data['html_form'] = render_to_string('tasks/includes/partial_task_delete.html', context, request=request)
    return JsonResponse(data)


# ----------------------------------------------------------------------------------------------------------------------
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def save_project_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            data['form_is_valid'] = True
            projects = Project.objects.all()
            data['html_task_list'] = render_to_string('projects/includes/partial_project_list.html', {'projects': projects})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
    else:
        form = ProjectForm()
    return save_project_form(request, form, 'projects/includes/partial_project_create.html')


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
    else:
        form = ProjectForm(instance=project)
    return save_project_form(request, form, 'projects/includes/partial_project_update.html')


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    data = dict()
    if request.method == 'POST':
        project.delete()
        data['form_is_valid'] = True
        projects = Project.objects.all()
        data['html_project_list'] = render_to_string('projects/includes/partial_project_list.html', {'projects': projects})
    else:
        context = {'project': project}
        data['html_form'] = render_to_string('projects/includes/partial_project_delete.html', context, request=request)
    return JsonResponse(data)


# ----------------------------------------------------------------------------------------------------------------------
def registration(request):
    args = {}
    args.update(csrf(request))
    args['form'] = MyUserCreationForm()
    if request.POST:
        new_user_form = MyUserCreationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()
            new_user = authenticate(username=new_user_form.cleaned_data['username'],
                                    password=new_user_form.cleaned_data['password2'])
            login(request, new_user)
            return redirect('/')
        else:
            print(new_user_form.errors)
            args['form'] = new_user_form
    return render_to_response('auth/registration.html', args)


def login_view(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            args['login error'] = "User not found"
            return render_to_response('auth/login.html', args)
    else:
        return render_to_response('auth/login.html', args)


def logout_view(request):
    logout(request)
    return redirect('/')


def reset_password(request):
    template_response = password_reset(request, template_name='auth/pwd_reset/password_reset_form.html',
                                       post_reset_redirect='password_reset_done')
    return template_response


class PasswordResetDone(TemplateView):
    template_name = 'auth/pwd_reset/password_reset_done.html'


def reset_password_confirm(request):
    template_response = password_reset_confirm(request, template_name='auth/pwd_reset/password_reset_confirm.html',
                                               post_reset_redirect='password_reset_complete')
    return template_response


def reset_password_complete(request):
    template_response = password_reset_complete(request, template_name='auth/pwd_reset/password_reset_complete.html')
    return template_response


class Profile(DetailView):
    model = User
    template_name = 'auth/profile/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'role']
    template_name = 'auth/profile/users_update_form.html'

    def get_success_url(self):
        return reverse_lazy('profile')


def change_password(request):
    template_response = password_change(request, template_name='auth/profile/password_change_form.html',
                                        post_change_redirect='profile')
    return template_response
