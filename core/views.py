from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from core.models import Week, Shift, Car, Driver, ExtraTax, Ride, PlanShift
from core.serializers import WeekSerializer, ShiftSerializer, CarSerializer, DriverSerializer, ExtraTaxSerializer, WriteRideSerializer, ReadRideSerializer, ReportRidesSerializer, ReportParamsSerializer, RegisterSerializer, UserSerializer
from core.reports import rides_report
from core.permissions import IsAdminOrReadOnly, AllowListPermission


class WeekListAPIView(ListAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Week.objects.all()
    serializer_class = WeekSerializer


class ShiftModelViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    renderer_classes = (JSONRenderer, XMLRenderer,)


class CarModelViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.select_related("user").filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class DriverModelViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = DriverSerializer
    pagination_class = None

    def get_queryset(self):
        # return Driver.objects.select_related("user").filter(user=self.request.user)
        return Driver.objects.select_related("user")

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ExtraTaxModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions & AllowListPermission,)   # or you can use '|' for 'OR'
    queryset = ExtraTax.objects.all()
    serializer_class = ExtraTaxSerializer


class RideModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("driver__name", "number", "car__plate")
    ordering_fields = ("shift", "number")
    filterset_fields = ("car__plate", "shift__week")

    def get_queryset(self):
        print(self.request.user)
        return Ride.objects.select_related("driver", "car", "shift", "extra_tax", "user").filter(user=self.request.user)
        # return Ride.objects.select_related("driver", "car", "shift", "extra_tax", "user")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadRideSerializer
        return WriteRideSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class RideReportAPIView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        params_serializer = ReportParamsSerializer(data=request.GET, context={"request": request})
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()
        data = rides_report(params)
        serializer = ReportRidesSerializer(instance=data, many=True)
        return Response(data=serializer.data)


class RegisterView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': '???????????????????????? ?????????????? ????????????',
        })


class ProfileView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            'user': UserSerializer(request.user, context=self.get_serializer_context()).data,
        })