from django.apps import AppConfig
from django.apps import apps
#CustomUser = apps.get_model('shop', 'Customer')


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
