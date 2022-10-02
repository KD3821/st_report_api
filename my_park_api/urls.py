from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from core import views
import debug_toolbar


router = routers.SimpleRouter()

router.register(r'shifts', views.ShiftModelViewSet, basename='shift')
router.register(r'cars', views.CarModelViewSet, basename='cars')
router.register(r'drivers', views.DriverModelViewSet, basename='drivers')
router.register(r'extratax', views.ExtraTaxModelViewSet, basename='extratax')
router.register(r'rides', views.RideModelViewSet, basename='rides')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', obtain_auth_token, name='obtain-auth-token'),
    path('weeks/', views.WeekListAPIView.as_view(), name='weeks'),
    path('report/', views.RideReportAPIView.as_view(), name='report'),
    path('__debug__/', include('debug_toolbar.urls')),
] + router.urls
