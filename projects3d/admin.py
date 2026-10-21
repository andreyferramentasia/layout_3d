from django.contrib import admin
from projects3d.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_file')
    search_fields = ('name')



admin.site.register(Project, ProjectAdmin)