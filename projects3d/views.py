from django.urls import reverse_lazy
from projects3d.forms import ProjectCreateForm, ProjectUpdateForm
from projects3d.models import Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = 'projects3d/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10 

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

class ProjectDetailView(LoginRequiredMixin,DetailView):
    model = Project
    template_name = 'projects3d/project_detail.html'
    context_object_name = 'project'

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects3d/project_create.html'
    context_object_name = 'project'
    success_url = reverse_lazy('projects3d:project-list')

class ProjectUpdateView(LoginRequiredMixin,UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'projects3d/project_update.html'
    context_object_name = 'project'
    success_url = reverse_lazy('projects3d:project-list')

class ProjectDeleteView(LoginRequiredMixin,DeleteView):
    model = Project
    template_name = 'projects3d/project_confirm_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('projects3d:project-list')