import math
from decimal import Decimal

from django.test import TestCase

from ..models import Airplane


class AirplaneModelTests(TestCase):

    def setUp(self) -> None:
        self.airplane, _ = Airplane.objects.get_or_create(
            id=2,
            passenger=80,
        )

    def get_fuel_tank_capacity(self) -> int:
        return self.airplane.MINIMUM_FUEL * self.airplane.id

    def get_airplane_fuel_consumption_per_minute(self) -> Decimal:
        return Decimal(math.log(self.airplane.id, 10)) * self.airplane.FUEL_CONSUMPTION

    def get_additional_fuel_consumption_from_passenger_per_minute(self) -> Decimal:
        return self.airplane.passenger * self.airplane.PASSENGER_FUEL_CONSUMPTION

    def get_total_fuel_consumption_per_minute(self) -> Decimal:
        airplane_fuel_consumption_per_minute = self.get_airplane_fuel_consumption_per_minute()
        additional_fuel_consumption_from_passenger_per_minute = (
            self.get_additional_fuel_consumption_from_passenger_per_minute()
        )
        return airplane_fuel_consumption_per_minute + additional_fuel_consumption_from_passenger_per_minute

    def test_fuel_tank_capacity(self) -> None:
        expected_result = self.get_fuel_tank_capacity()
        actual_result = self.airplane.get_fuel_tank_capacity()

        self.assertEqual(
            actual_result,
            expected_result,
            f"Expected result is {expected_result} but method returns {actual_result}"
        )

    def test_airplane_fuel_consumption_per_minute(self) -> None:
        expected_result = self.get_airplane_fuel_consumption_per_minute()
        actual_result = self.airplane.get_airplane_fuel_consumption_per_minute()

        self.assertEqual(
            actual_result,
            expected_result,
            f"Expected result is {expected_result} but method returns {actual_result}"
        )

    def test_additional_fuel_consumption_from_passenger_per_minute(self) -> None:
        expected_result = self.get_additional_fuel_consumption_from_passenger_per_minute()
        actual_result = self.airplane.get_additional_fuel_consumption_from_passenger_per_minute()

        self.assertEqual(
            actual_result,
            expected_result,
            f"Expected result is {expected_result} but method returns {actual_result}"
        )

    def test_total_fuel_consumption_per_minute(self) -> None:
        expected_result = self.get_total_fuel_consumption_per_minute()
        actual_result = self.airplane.get_total_fuel_consumption_per_minute()

        self.assertEqual(
            actual_result,
            expected_result,
            f"Expected result is {expected_result} but method returns {actual_result}"
        )

    def test_maximum_minutes_to_fly(self):
        expected_result = self.get_fuel_tank_capacity() / self.get_total_fuel_consumption_per_minute()
        actual_result = self.airplane.get_maximum_minutes_to_fly()

        self.assertEqual(
            actual_result,
            expected_result,
            f"Expected result is {expected_result} but method returns {actual_result}"
        )

    def tearDown(self) -> None:
        self.airplane.delete()
