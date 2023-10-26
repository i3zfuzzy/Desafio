import requests
import numpy as np
from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Q
from .models import ExchangeRate


# Verifica o range entre datas
def get_datas_between_period(date_i, date_e):
    date_i = datetime.strptime(date_i, "%Y-%m-%d")
    date_e = datetime.strptime(date_e, "%Y-%m-%d")

    dates_between_period = [date_i]

    while date_i < date_e:
        date_i += timedelta(days=1)
        dates_between_period.append(date_i)

    return dates_between_period


# Verifica finais de semana
def is_business_days(date):
    if date.weekday() >= 5:
        return False
    return True


# Verifica range de 5 dias úteis
def date_range(date_s, date_e):
    date_s = datetime.strptime(date_s, "%Y-%m-%d")
    date_e = datetime.strptime(date_e, "%Y-%m-%d")
    actual_day = date_s
    business_day = 0

    while actual_day <= date_e and business_day < 5:
        if is_business_days(actual_day):
            business_day += 1
        actual_day += timedelta(days=1)

    return business_day <= 5


def fetch_and_save_exchange_rates(start_date, end_date):
    base_url = "https://api.vatcomply.com/rates"
    currencies = ["EUR", "JPY", "BRL"]
    dates_between_period = get_datas_between_period(start_date, end_date)
    for date in dates_between_period:
        if not ExchangeRate.objects.filter(date=date).exists():
            for currency in currencies:
                response = requests.get(f"{base_url}?date={start_date}&base=USD")
                data = response.json()
                ExchangeRate.objects.create(
                    date=start_date,
                    base_currency="USD",
                    target_currency=currency,
                    rate=data["rates"][currency]
                )
            break


def get_exchange_rate_data(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if date_range(start_date, end_date):
        dates_between_period = get_datas_between_period(start_date, end_date)
        for date in dates_between_period:
            fetch_and_save_exchange_rates(date.strftime("%Y-%m-%d"), end_date)
    data = ExchangeRate.objects.filter(Q(date__gte=start_date), Q(date__lte=end_date))
    print(data)
    return render(request, 'vat_manager/index.html', {'data': data})
