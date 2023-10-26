from django.urls import path
from vat_manager.views import get_exchange_rate_data

name_app = 'vat_manager'


urlpatterns = [
    path('get_exchange_rate_data', get_exchange_rate_data, name='consultar_cotacoes'),
]


