import requests

from datetime import datetime, timedelta
from django.core.management import BaseCommand

from ...models import Currency


def get_bmx_data_series(id_serie, date_start, date_end):
    data = None
    today = datetime.now()
    yesterday = today - timedelta(days=20)

    date_initial = date_start if date_start else yesterday.strftime("%Y-%m-%d")
    date_final = date_end if date_end else today.strftime("%Y-%m-%d")

    payload = {"token": "1ba45f2994e44d4bfcf76fb4dc59da324fe759dfed9b3f765a01f8adff26e7e6"}
    url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{id_serie}/datos/{date_initial}/{date_final}'
    r = requests.get(url, params=payload)
    if r.status_code == 200:
        response = r.json()
        data = response.get("bmx").get("series")[0].get("datos", None)
    return data

def create_data_series(id_serie, data):
    id_kind = 1 if id_serie == "SP68257" else 2

    for currency in data:
        for k, v in currency.items():
            if k == "fecha":
                date = v
            value = v
        print(date, value)
        Currency.objects.get_or_create(date=datetime.strptime(date, '%d/%m/%Y'), value=value, kind=id_kind)
    

class Command(BaseCommand):
    def add_arguments(self, parser):
        """ Define custom arguments that will be taken in the script """
        parser.add_argument('-di', '--date_start', type=str, help="Define a date initial")
        parser.add_argument('-df', '--date_end', type=str, help="Define a date final")

    def handle(self, *args, **kwargs):
        date_start = kwargs.get("date_start", None)
        date_end = kwargs.get("date_end", None)

        # UDIS = SP68257
        # DOLAR = SF63528
        series = ["SP68257", "SF63528"]
       
        for id_serie in series:
            data = get_bmx_data_series(id_serie, date_start, date_end)
            if data:
                create_data_series(id_serie, data)
