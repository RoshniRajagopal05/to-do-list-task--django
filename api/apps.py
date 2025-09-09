from django.apps import AppConfig



class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        from .taskscheduler import start_scheduler
        start_scheduler()