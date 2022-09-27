from django.urls import path
from rest_framework import routers
from core import views


router = routers.SimpleRouter()

router.register(r'shifts', views.ShiftModelViewSet, basename='shift')
router.register(r'cars', views.CarModelViewSet, basename='cars')
router.register(r'drivers', views.DriverModelViewSet, basename='drivers')
router.register(r'extratax', views.ExtraTaxModelViewSet, basename='extratax')
router.register(r'rides', views.RideModelViewSet, basename='rides')

urlpatterns = [
    path('weeks/', views.WeekListAPIView.as_view(), name='weeks'),
] + router.urls
