"""leverX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from leverapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^registration/$', views.registration, name='registration'),

    url(r'^reset/password_reset/$', views.reset_password, name='password_reset'),
    url(r'^reset/password_reset/done/$', views.PasswordResetDone.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.reset_password_complete, name='password_reset_complete'),

    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^profile/update/(?P<pk>\d+)/$', views.ProfileUpdate.as_view(), name='update'),
    url(r'^profile/password_change/$', views.change_password, name='password_change'),

    url(r'^developers/$', views.developer_list, name='developer_list'),

    url(r'^tasks/$', views.task_list, name='task_list'),
    url(r'^tasks/create/$', views.task_create, name='task_create'),
    url(r'^tasks/(?P<pk>\d+)/update/$', views.task_update, name='task_update'),
    url(r'^tasks/(?P<pk>\d+)/delete/$', views.task_delete, name='task_delete'),

    url(r'^projects/$', views.project_list, name='project_list'),
    url(r'^projects/create/$', views.project_create, name='project_create'),
    url(r'^projects/(?P<pk>\d+)/update/$', views.project_update, name='project_update'),
    url(r'^projects/(?P<pk>\d+)/delete/$', views.project_delete, name='project_delete'),
]
