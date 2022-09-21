from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.reports'
    label: str = 'reports'
    
    def ready(self):
        from api.v1.users import (
            handlers,
        )
    
