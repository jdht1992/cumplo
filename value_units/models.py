from django.db import models

KIND = (
        (1, 'UDI'),
        (2, 'DOLAR'),
    )

class Currency(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=6)
    kind = models.PositiveSmallIntegerField(choices=KIND, default=1)

    def __str__(self):
        return f"{self.kind}"
