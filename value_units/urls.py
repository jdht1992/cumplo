from django.urls import path
from .views import CurrencyList

urlpatterns = [
    path("", CurrencyList.as_view(), name="pie-chart"),
]