from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from core import views


router = routers.SimpleRouter()

router.register(r'shifts', views.ShiftModelViewSet, basename='shift')
router.register(r'cars', views.CarModelViewSet, basename='cars')
router.register(r'drivers', views.DriverModelViewSet, basename='drivers')
router.register(r'extratax', views.ExtraTaxModelViewSet, basename='extratax')
router.register(r'rides', views.RideModelViewSet, basename='rides')

urlpatterns = [
    path('login/', obtain_auth_token, name='obtain-auth-token'),
    path('weeks/', views.WeekListAPIView.as_view(), name='weeks'),
    path('report/', views.RideReportAPIView.as_view(), name='report'),
] + router.urls
