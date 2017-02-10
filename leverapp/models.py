from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import datetime


class User(AbstractUser):
    MANAGER = 1
    DEVELOPER = 2
    JOB_TYPES = (
        (MANAGER, 'Manager'),
        (DEVELOPER, 'Developer'),
    )
    role = models.PositiveSmallIntegerField(choices=JOB_TYPES)

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Task(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    due_date = models.DateField(default=datetime.now())
    developer = models.ForeignKey(User, blank=False)

    def __str__(self):
        return '{}'.format(self.title)


class Project(models.Model):
    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    managers = models.ManyToManyField(User)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return '{}'.format(self.title)




