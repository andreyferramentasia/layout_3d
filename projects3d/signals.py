from django.db.models.signals import post_delete
from django.dispatch import receiver
from projects3d.models import Project

@receiver(post_delete, sender=Project)
def delete_project_files(sender, instance, **kwargs):
    if instance.model_file:
        instance.model_file.delete(save=False)