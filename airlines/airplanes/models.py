import math
from decimal import Decimal

from django.db import models

from airlines.core.models import Audit


class Airplane(Audit):

    MINIMUM_FUEL = Decimal(200)
    FUEL_CONSUMPTION = Decimal(0.8)
    PASSENGER_FUEL_CONSUMPTION = Decimal(0.002)

    id = models.IntegerField(primary_key=True)
    passenger = models.IntegerField()

    def get_fuel_tank_capacity(self) -> int:
        return self.MINIMUM_FUEL * Decimal(self.id)

    def get_airplane_fuel_consumption_per_minute(self) -> Decimal:
        return Decimal(math.log(self.id, 10)) * self.FUEL_CONSUMPTION

    def get_additional_fuel_consumption_from_passenger_per_minute(self) -> Decimal:
        return self.passenger * self.PASSENGER_FUEL_CONSUMPTION

    def get_total_fuel_consumption_per_minute(self) -> Decimal:
        return (
            self.get_airplane_fuel_consumption_per_minute()
            + self.get_additional_fuel_consumption_from_passenger_per_minute()
        )

    def get_maximum_minutes_to_fly(self):
        return self.get_fuel_tank_capacity() / self.get_total_fuel_consumption_per_minute()
