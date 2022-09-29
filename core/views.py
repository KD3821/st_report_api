from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Week, Shift, Car, Driver, ExtraTax, Ride
from core.serializers import WeekSerializer, ShiftSerializer, CarSerializer, DriverSerializer, ExtraTaxSerializer, WriteRideSerializer, ReadRideSerializer


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
    pagination_class = None


class ExtraTaxModelViewSet(ModelViewSet):
    queryset = ExtraTax.objects.all()
    serializer_class = ExtraTaxSerializer


class RideModelViewSet(ModelViewSet):
    queryset = Ride.objects.select_related("driver", "car", "shift", "extra_tax")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("driver__name",)
    ordering_fields = ("shift", "number")
    filterset_fields = ("car__plate",)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadRideSerializer
        return WriteRideSerializer