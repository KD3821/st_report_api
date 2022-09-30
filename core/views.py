from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Week, Shift, Car, Driver, ExtraTax, Ride
from core.serializers import WeekSerializer, ShiftSerializer, CarSerializer, DriverSerializer, ExtraTaxSerializer, WriteRideSerializer, ReadRideSerializer, ReportRidesSerializer, ReportParamsSerializer
from core.reports import rides_report


class WeekListAPIView(ListAPIView):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer


class ShiftModelViewSet(ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class CarModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.select_related("user").filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class DriverModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DriverSerializer
    pagination_class = None

    def get_queryset(self):
        return Driver.objects.select_related("user").filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ExtraTaxModelViewSet(ModelViewSet):
    queryset = ExtraTax.objects.all()
    serializer_class = ExtraTaxSerializer


class RideModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("driver__name",)
    ordering_fields = ("shift", "number")
    filterset_fields = ("car__plate",)

    def get_queryset(self):
        return Ride.objects.select_related("driver", "car", "shift", "extra_tax", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadRideSerializer
        return WriteRideSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class RideReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params_serializer = ReportParamsSerializer(data=request.GET, context={"request": request})
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()
        data = rides_report(params)
        serializer = ReportRidesSerializer(instance=data, many=True)
        return Response(data=serializer.data)