from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.users'
    label: str = 'users'
    
    def ready(self):
        from api.v1.users import (
            handlers,
        )
