from django.apps import AppConfig


class DairyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dairyapp'
    verbose_name = 'Dairy Management System'
    
    def ready(self):
        """
        Perform initialization tasks when the app is ready.
        """
        # Import signals to register them
        import dairyapp.signals
        
        # If you have scheduled tasks (using django-celery-beat)
        # from django_celery_beat.models import PeriodicTask
        # from django_celery_beat.schedulers import DatabaseScheduler
        # ...
        
        # If you need to run startup code only once
        # if not getattr(self, '_ready_called', False):
        #     self._ready_called = True
        #     self.startup_tasks()
    
    def startup_tasks(self):
        """
        Run tasks when the application starts.
        """
        # Example: Clear expired sessions
        # from django.contrib.sessions.models import Session
        # Session.objects.filter(expire_date__lt=timezone.now()).delete()
        pass