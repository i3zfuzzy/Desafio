from django.db import models


class ExchangeRate(models.Model):
    date = models.DateField()
    base_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    rate = models.FloatField()

    objects = models.Manager()

    def __str__(self):
        return f'Date: {self.date}, base_currency: {self.base_currency}, target_currency: {self.target_currency}, rate: {self.rate}'
