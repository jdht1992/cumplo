from django.contrib import admin
from .models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'value', 'kind')


admin.site.register(Currency, CurrencyAdmin)
