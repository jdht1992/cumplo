import datetime

from django.shortcuts import render
from django.db.models import Avg, Max, Min
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View

from .models import Currency, KIND


class CurrencyView(View):
    paginate_by = 10
    template_name = "currency/currency_list.html"
    CURRENCY = {"UDI": 1, "DOLLAR": 2}  # Cambialo a plural

    def get(self, request):
        date_start = request.GET.get("date_start", None)
        date_end = request.GET.get("date_end", None)
        kind = request.GET.get("kind", None)
        page = request.GET.get("page")
        context = {}

        if kind and date_start and date_end:
            queryset = self._get_queryset(kind, date_start, date_end)
            paginated = self._get_paginator(queryset, page)
            context = self._get_context(queryset, paginated)

        return render(request, self.template_name, context)

    def _get_queryset(self, kind, date_start, date_end):
        """Return a filtered queryset using the parameters given.
        :param kind: str (1=UDIS, 2=DOLLAR)
        :param date_start: str  YYYY-MM-DD
        :param date_end: str YYYY-MM-DD
        :return: queryset
        """
        parameters = {
            "kind": self.CURRENCY.get(kind),
            "date__gte": self._convert_str_datetime(date_start),
            "date__lte": self._convert_str_datetime(date_end),
        }
        return Currency.objects.filter(**parameters).order_by("date")

    def _convert_str_datetime(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%d")

    def _get_paginator(self, queryset, page):
        """ Return a list of items with paginated results. 
        :param queryset: queryset filtered
        :param page: Page number
        :return: context
        """
        paginator = Paginator(queryset, self.paginate_by)

        try:
            paginated = paginator.get_page(page)
        except PageNotAnInteger:
            paginated = paginator.get_page(1)
        except EmptyPage:
            paginated = paginator.page(paginator.num_pages)

        return paginated

    def _get_context(self, queryset, paginated):
        """Return multiple context that will be used in template of this view.
        :param queryset: queryset filtered
        :param paginated: Paginator object
        :return: objects paginered
        """
        context = {
            "currencies": paginated,
            "average": queryset.aggregate(Avg("value")).get("value__avg", 0),
            "max": queryset.aggregate(Max("value")).get("value__max", 0),
            "min": queryset.aggregate(Min("value")).get("value__min", 0),
            "date": self._get_range_dates(queryset),
            "value": self._get_range_values(queryset),
        }
        return context

    def _get_range_dates(self, queryset):
        return [str(date) for date in queryset.values_list("date", flat=True)]

    def _get_range_values(self, queryset):
        return [float(value) for value in queryset.values_list("value", flat=True)]
