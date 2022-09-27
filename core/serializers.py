from rest_framework import serializers
from core.models import Week, Shift, Car, Driver, ExtraTax, Ride, PlanShift


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'plate',)


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('name',)


class ExtraTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraTax
        fields = '__all__'


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'


class PlanShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanShift
        fields = '__all__'