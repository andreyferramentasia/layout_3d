from django.urls import path
from projects3d.views import ProjectDeleteView, ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView

app_name = 'projects3d'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('detail/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),
]