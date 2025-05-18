from django.apps import AppConfig


class RepositoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repository'
    
    def ready(self):
        import repository.signals  # Import signals 