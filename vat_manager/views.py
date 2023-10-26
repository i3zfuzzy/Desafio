from collections import defaultdict
from datetime import datetime, timedelta
import aiohttp
from django.db.models import Q, Max
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import asyncio
from django.views import View

from .models import ExchangeRate


# Verifica o range entre datas, e complementa data inicio até data fim para request
def get_datas_between_period(date_i, date_e):
    date_i = datetime.strptime(date_i, "%Y-%m-%d")
    date_e = datetime.strptime(date_e, "%Y-%m-%d")

    dates_between_period = [date_i]

    while date_i < date_e:
        date_i += timedelta(days=1)
        dates_between_period.append(date_i)

    return dates_between_period


# Verifica range de 5 dias úteis
def date_range(date_s, date_e):
    date_s = datetime.strptime(date_s, "%Y-%m-%d")
    date_e = datetime.strptime(date_e, "%Y-%m-%d")
    business_day = 0
    actual_day = date_s

    while actual_day <= date_e:
        if actual_day.weekday() < 5:
            business_day += 1
        actual_day += timedelta(days=1)

    return business_day <= 5


# Valida o range de data da request, salva o objeto no banco
async def fetch_exchange_rate(session, date, base_url, currency):
    async with session.get(f"{base_url}?date={date}&base=USD") as response:
        data = await response.json()
        return data["rates"][currency]


async def fetch_and_save_exchange_rates(start_date, end_date):
    base_url = "https://api.vatcomply.com/rates"
    currencies = ["EUR", "JPY", "BRL"]
    dates_between_period = get_datas_between_period(start_date, end_date)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for date in dates_between_period:
            if not ExchangeRate.objects.filter(date=date).exists():
                for currency in currencies:
                    task = asyncio.create_task(fetch_exchange_rate(session, date, base_url, currency))
                    tasks.append(task)

        results = await asyncio.gather(*tasks)

        for i, date in enumerate(dates_between_period):
            if not ExchangeRate.objects.filter(date=date).exists():
                for j, currency in enumerate(currencies):
                    ExchangeRate.objects.create(
                        date=date,
                        base_currency="USD",
                        target_currency=currency,
                        rate=results[i * len(currencies) + j]
                    )


# Recebe a request do usuário e monta a base de dados do gráfico
def get_exchange_rate_data(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if date_range(start_date, end_date):
        dates_between_period = get_datas_between_period(start_date, end_date)
        for date in dates_between_period:
            fetch_and_save_exchange_rates(date.strftime("%Y-%m-%d"), end_date)
    else:
        return HttpResponse("Data informada não correponde à 5 dias úteis")

    data = ExchangeRate.objects.filter(Q(date__gte=start_date), Q(date__lte=end_date))
    unique_dates = data.values('date').annotate(Max('date'))
    unique_data = [str(datum['date__max']) for datum in unique_dates]

    currency_rates = defaultdict(list)

    for datum in data:
        currency_rates[datum.target_currency].append(datum.rate)

    usd_to_eur = currency_rates['EUR']
    usd_to_brl = currency_rates['BRL']
    usd_to_jpy = currency_rates['JPY']

    return render(request, 'vat_manager/index.html',
                  {'dates': unique_data, 'usd_to_eur': usd_to_eur, 'usd_to_brl': usd_to_brl, 'usd_to_jpy': usd_to_jpy})


# Retorna todas as cotaçoes persistidas no banco
class TableView(View):
    def get(self, request):
        data = list(ExchangeRate.objects.values())
        return JsonResponse(data, safe=False)
