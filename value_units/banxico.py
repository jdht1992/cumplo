from datetime import datetime, timedelta

import requests

from value_units.models import Currency
from value_units.views import convert_str_datetime


class Banxico:
    TIMEOUT = 15
    SERIES = {"SP68257": 1, "SF63528": 2}

    def get_response_date_range(self, type_currency, date_start, date_end):
        """validate and assign value of dates, return the response of the api
        :param type_currency: str SP68257
        :param date_start: str  YYYY-MM-DD
        :param date_end: str YYYY-MM-DD
        :return: list []
        """
        if not date_start and not date_end:
            today = datetime.now()
            yesterday = today - timedelta(days=1)

            date_start = convert_str_datetime(yesterday)
            date_end = convert_str_datetime(today)

        response = self._request_data(type_currency, date_start, date_end)

        return response

    def _request_data(self, type_currency, date_start, date_end):
        """makes requests to the api of bank of mexico for retrieve information about different series value
        :param type_currency: str SP68257
        :param date_start: str  YYYY-MM-DD
        :param date_end: str YYYY-MM-DD
        :return: list []
        """
        data = []
        try:
            response = requests.get(
                url=self._get_url(type_currency, date_start, date_end),
                params=self._get_parameters(),
                timeout=self.TIMEOUT,
            )
            if response.status_code == 200:
                data = response.json().get("bmx").get("series")[0].get("datos", None)
        except (IndexError, ValueError):
            print("Error: list index out of range")
        except Exception as err:
            print(f"Other error occurred: {err}")

        return data

    def _get_parameters(self):
        return {
            "token": "1ba45f2994e44d4bfcf76fb4dc59da324fe759dfed9b3f765a01f8adff26e7e6"
        }

    def _get_url(self, type_currency, date_start, date_end):
        return f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{type_currency}/datos/{date_start}/{date_end}"
