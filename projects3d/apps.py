from django.apps import AppConfig

class Projects3DConfig(AppConfig):
    name = 'projects3d'

    def ready(self):
        import projects3d.signals  # noqa: F401
