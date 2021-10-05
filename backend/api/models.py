from django.db import models
from djmoney.models.fields import MoneyField

class Statistics(models.Model):
    date = models.DateField()
    views = models.PositiveIntegerField(null=True)
    clicks = models.PositiveIntegerField(null=True)
    cost = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB', null=True)
    cpc = models.DecimalField(max_digits=12, decimal_places=7)
    cpm = models.DecimalField(max_digits=17, decimal_places=4)

    def __str__(self):
        return "{}".format(self.date)
