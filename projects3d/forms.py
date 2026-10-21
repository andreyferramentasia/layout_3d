from django import forms
from projects3d.models import Project


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'model_file']
 


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'model_file']