import datetime

from django.core.management import BaseCommand

from value_units.models import Currency
from value_units.banxico import Banxico


def convert_str_datetime(date):
    return datetime.datetime.strptime(date, "%d/%m/%Y")


def create_currency(type_currency, data):
    """ create new currency object """

    for currency in data:
        Currency.objects.get_or_create(
            date=convert_str_datetime(currency["fecha"]),
            value=currency["dato"],
            kind=type_currency,
        )


class Command(BaseCommand):
    CURRENCIES = {"UDIS": "SP68257", "DOLLAR": "SF63528"}

    def add_arguments(self, parser):
        """ Define custom arguments that will be taken in the script """

        parser.add_argument(
            "--date_start", type=str, help="Define a date initial"
        )  # --date_init --date_start
        parser.add_argument("--date_end", type=str, help="Define a date final")
        parser.add_argument("--kind", type=str, help="Define a kind serie")

    def handle(self, *args, **kwargs):
        """ take the arguments that will be used to make the request to the api of the bank of mexico """

        date_start = kwargs.get("date_start", None)
        date_end = kwargs.get("date_end", None)
        kind = kwargs.get("kind", None)

        series = [self.CURRENCIES.get("UDIS"), self.CURRENCIES.get("DOLLAR")]
        if kind:
            series = [self.CURRENCIES.get(kind)]

        for serie in series:
            banxico = Banxico()
            data = banxico.get_response_date_range(serie, date_start, date_end)
            if data:
                create_currency(self._get_type_currency(serie), data)

    def _get_type_currency(self, serie):
        SERIES = {"SP68257": 1, "SF63528": 2}
        return SERIES[serie]
