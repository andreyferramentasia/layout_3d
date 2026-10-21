from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    model_file = models.FileField(upload_to='projects3d/models/', blank=True)
    

    def __str__(self):
        return self.name