import requests
from datetime import datetime, timedelta

from django.core.management import BaseCommand

from ...models import Currency


def request_data_of_bmx_api(id_serie, date_initial, date_final):
    """ makes requests to the api of bank of mexico for retrieve information about different series value """
    
    data = None
    payload = {"token": "1ba45f2994e44d4bfcf76fb4dc59da324fe759dfed9b3f765a01f8adff26e7e6"}
    url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{id_serie}/datos/{date_initial}/{date_final}'

    try:
        r = requests.get(url, params=payload, timeout=15)
        if r.status_code == 200:
            response = r.json()
            data = response.get("bmx").get("series")[0].get("datos", None)

    # If the response was successful, no Exception will be raised
    except (IndexError, ValueError):
        print('Error: list index out of range')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return data

def get_data_of_bmx(id_serie, date_start, date_end):
    """ validate and assign value of dates, return the response of the api """
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    date_initial = date_start if date_start else yesterday.strftime("%Y-%m-%d")
    date_final = date_end if date_end else today.strftime("%Y-%m-%d")

    res = request_data_of_bmx_api(id_serie, date_initial, date_final)
    
    return res

def create_currency(id_serie, data):
    """ create new currency  object """
    
    id_kind = 1 if id_serie == "SP68257" else 2

    for currency in data:
        for k, v in currency.items():
            if k == "fecha":
                date = v
            value = v
        print(id_kind, date, value)
        Currency.objects.get_or_create(date=datetime.strptime(date, '%d/%m/%Y'), value=value, kind=id_kind)
    

class Command(BaseCommand):
    def add_arguments(self, parser):
        """ Define custom arguments that will be taken in the script """
        
        parser.add_argument('-di', '--date_start', type=str, help="Define a date initial")
        parser.add_argument('-df', '--date_end', type=str, help="Define a date final")
        parser.add_argument('-kind', '--kind', type=str, help="Define a kind serie")

    def handle(self, *args, **kwargs):
        """ take the arguments that will be used to make the request to the api of the bank of mexico """
        
        UDIS, DOLLAR = ["SP68257"], ["SF63528"]

        date_start = kwargs.get("date_start", None)
        date_end = kwargs.get("date_end", None)
        kind = kwargs.get("kind", None)
        
        if kind:
            series = UDIS if kind == "UDIS" else DOLLAR
        else:
            series = ["SP68257", "SF63528"]
       
        for id_serie in series:
            data = get_data_of_bmx(id_serie, date_start, date_end)
            if data:
                create_currency(id_serie, data)
