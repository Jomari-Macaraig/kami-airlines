from rest_framework import generics

from .serializers import AirplaneSerializer
from ..models import Airplane


class AirplaneList(generics.ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
