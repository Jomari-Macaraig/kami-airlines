import math
from decimal import Decimal, getcontext
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.response import Response

from ..models import Airplane


getcontext().prec = 8


class AirplaneAPITests(TestCase):

    def setUp(self) -> None:
        self.airplane, _ = Airplane.objects.get_or_create(
            id=2,
            passenger=80,
        )
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.minimum_fuel = Airplane.MINIMUM_FUEL
        self.fuel_consumption = Airplane.FUEL_CONSUMPTION
        self.passenger_fuel_consumption = Airplane.PASSENGER_FUEL_CONSUMPTION

    def create_airplane(self, id: int, passenger: int) -> Response:
        response = self.client.post(
            reverse("apiv1:airplane"),
            {
                "id": id,
                "passenger": passenger
            }
        )
        return response

    def delete_airplane(self, id):
        try:
            airplane = Airplane.objects.get(pk=id)
        except Airplane.DoesNotExist:
            pass
        else:
            airplane.delete()

    def get_fuel_tank_capacity(self, id: int) -> int:
        return self.minimum_fuel * id

    def get_airplane_fuel_consumption_per_minute(self, id: int) -> Decimal:
        return Decimal(math.log(id, 10)) * self.fuel_consumption

    def get_additional_fuel_consumption_from_passenger_per_minute(self, passenger: int) -> Decimal:
        return passenger * self.passenger_fuel_consumption

    def get_total_fuel_consumption_per_minute(self, id: int, passenger: int) -> Decimal:
        airplane_fuel_consumption_per_minute = self.get_airplane_fuel_consumption_per_minute(id=id)
        additional_fuel_consumption_from_passenger_per_minute = (
            self.get_additional_fuel_consumption_from_passenger_per_minute(passenger=passenger)
        )
        return airplane_fuel_consumption_per_minute + additional_fuel_consumption_from_passenger_per_minute

    def test_fields(self) -> None:
        expected_fields = {
            "id",
            "passenger",
            "total_fuel_consumption_per_minute",
            "maximum_minutes_to_fly",
        }
        response = self.client.get(reverse("apiv1:airplane"))
        actual_fields = set(response.json()[0].keys())
        self.assertEqual(
            expected_fields,
            actual_fields,
            f"Expected list of fields {expected_fields} but API returned  {actual_fields}"
        )

    def test_create_airplane(self) -> None:
        id = 3
        passenger = 80
        response = self.create_airplane(id=id, passenger=80)
        self.assertEqual(
            status.HTTP_201_CREATED,
            response.status_code,
            f"Status code returned not {status.HTTP_201_CREATED}"
        )
        data = response.json()
        self.assertEqual(
            id,
            data["id"],
            f"Id of the airplane is not {id}"
        )
        self.assertEqual(
            passenger,
            data["passenger"],
            f"Passenger count of airplane is not {passenger}"
        )
        self.delete_airplane(id=id)

    def test_total_fuel_consumption_per_minute(self) -> None:
        id = 4
        passenger = 80
        expected_result = self.get_total_fuel_consumption_per_minute(id=id, passenger=passenger)
        response = self.create_airplane(id=id, passenger=80)
        data = response.json()
        actual_result = data["total_fuel_consumption_per_minute"]

        self.assertEqual(
            f"{expected_result:.8f}",
            actual_result,
            f"Expected result is {expected_result} but API returns {actual_result}"
        )

        self.delete_airplane(id=id)

    def test_maximum_minuets_to_fly(self) -> None:
        id = 5
        passenger = 80

        expected_result = (
            self.get_fuel_tank_capacity(id=id) / self.get_total_fuel_consumption_per_minute(id=id, passenger=passenger)
        )
        response = self.create_airplane(id=id, passenger=80)
        data = response.json()
        actual_result = data["maximum_minutes_to_fly"]
        self.assertEqual(
            f"{expected_result:.8f}",
            actual_result,
            f"Expected result is {expected_result} but API returns {actual_result}"
        )

        self.delete_airplane(id=id)

    def tearDown(self) -> None:
        self.airplane.delete()
