from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from core.models import Week, Shift, Car, Driver, ExtraTax, Ride
from core.serializers import WeekSerializer, ShiftSerializer, CarSerializer, DriverSerializer, ExtraTaxSerializer, RideSerializer


class WeekListAPIView(ListAPIView):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer


class ShiftModelViewSet(ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class CarModelViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class DriverModelViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class ExtraTaxModelViewSet(ModelViewSet):
    queryset = ExtraTax.objects.all()
    serializer_class = DriverSerializer


class RideModelViewSet(ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer