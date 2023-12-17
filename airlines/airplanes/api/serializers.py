from rest_framework import serializers

from ..models import Airplane


class AirplaneSerializer(serializers.ModelSerializer):
    total_fuel_consumption_per_minute = serializers.DecimalField(
        source="get_total_fuel_consumption_per_minute",
        read_only=True,
        decimal_places=8,
        max_digits=10
    )
    maximum_minutes_to_fly = serializers.DecimalField(
        source="get_maximum_minutes_to_fly",
        read_only=True,
        decimal_places=8,
        max_digits=100
    )

    class Meta:
        model = Airplane
        fields = (
            "id",
            "passenger",
            "total_fuel_consumption_per_minute",
            "maximum_minutes_to_fly"
        )