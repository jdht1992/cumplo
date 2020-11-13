from django.shortcuts import render
from django.views.generic import ListView
from .models import Currency
from django.db.models import Avg, Max, Min
import datetime


class CurrencyList(ListView):
    paginate_by = 10
    template_name = 'currency/currency_list.html'
    context_object_name = 'currencies'

    def get_queryset(self):
        queryset = Currency.objects.none()
        date_end = self.request.GET.get("date_end", None)
        date_start = self.request.GET.get("date_start", None)
        kind = self.request.GET.get("kind", None)

        if kind and date_start and date_end:
            date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
            date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d')
            kind = 1 if kind == "UDI" else 2
            queryset = Currency.objects.filter(kind=kind, date__gte=date_start, date__lte=date_end)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["value_avg"] = self.get_queryset().aggregate(Avg('value')).get("value__avg")
        context["value_max"] = self.get_queryset().aggregate(Max('value')).get('value__max', 0)
        context["value_min"] = self.get_queryset().aggregate(Min('value')).get("value__min", 0)
        # context["labels"] = list(self.get_queryset().values_list("date", flat=True).order_by("date"))
        # context["value"] = list(self.get_queryset().values_list("value", flat=True).order_by("date"))
        context["date"] = [str(dt) for dt in self.get_queryset().values_list('date', flat=True)]
        context["value"] = [float(dt) for dt in self.get_queryset().values_list('value', flat=True)]
        return context
