from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from core import views
import debug_toolbar
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.SimpleRouter()

router.register(r'shifts', views.ShiftModelViewSet, basename='shift')
router.register(r'cars', views.CarModelViewSet, basename='cars')
router.register(r'drivers', views.DriverModelViewSet, basename='drivers')
router.register(r'extratax', views.ExtraTaxModelViewSet, basename='extratax')
router.register(r'rides', views.RideModelViewSet, basename='rides')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', obtain_auth_token, name='obtain-auth-token'),
    path('weeks/', views.WeekListAPIView.as_view(), name='weeks'),
    path('report/', views.RideReportAPIView.as_view(), name='report'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
] + router.urls
