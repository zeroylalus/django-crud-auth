from django.contrib import admin
from task import models

class Taskadmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(models.Task, Taskadmin)
