from django.apps import AppConfig
import os


class MesasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mesas'

    path = os.path.dirname(__file__)
