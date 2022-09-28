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
        fields = ('id', 'name',)


class ExtraTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraTax
        fields = '__all__'


class WriteRideSerializer(serializers.ModelSerializer):
    driver = serializers.SlugRelatedField(slug_field="name", queryset=Driver.objects.all())
    car = serializers.SlugRelatedField(slug_field="plate", queryset=Car.objects.all())
    shift = serializers.SlugRelatedField(slug_field="date", queryset=Shift.objects.all())
    extra_tax = serializers.SlugRelatedField(slug_field="mode", queryset=ExtraTax.objects.all())

    class Meta:
        model = Ride
        fields = (
            'number',
            'driver',
            'car',
            'shift',
            'price',
            'tip',
            'cash',
            'toll',
            'save_tax',
            'saved_tax_result',
            'extra_tax',
            'tax_result',
            'comment'
        )


class ReadRideSerializer(serializers.ModelSerializer):
    driver = serializers.SlugRelatedField(slug_field="name", queryset=Driver.objects.all())
    car = serializers.SlugRelatedField(slug_field="plate", queryset=Car.objects.all())
    shift = ShiftSerializer()
    extra_tax = ExtraTaxSerializer()

    class Meta:
        model = Ride
        fields = (
            'id',
            'number',
            'driver',
            'car',
            'shift',
            'price',
            'tip',
            'cash',
            'toll',
            'save_tax',
            'saved_tax_result',
            'extra_tax',
            'tax_result',
            'comment'
        )
        read_only_fields = fields


class PlanShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanShift
        fields = '__all__'