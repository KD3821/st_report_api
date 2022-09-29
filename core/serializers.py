from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Week, Shift, Car, Driver, ExtraTax, Ride, PlanShift


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')
        read_only_fields = fields


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = ('id', 'plate', 'user',)


class DriverSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Driver
        fields = ('id', 'name', 'user',)


class ExtraTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraTax
        fields = '__all__'


class WriteRideSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    driver = serializers.SlugRelatedField(slug_field="name", queryset=Driver.objects.all())
    car = serializers.SlugRelatedField(slug_field="plate", queryset=Car.objects.all())
    shift = serializers.SlugRelatedField(slug_field="date", queryset=Shift.objects.all())
    extra_tax = serializers.SlugRelatedField(slug_field="mode", queryset=ExtraTax.objects.all())

    class Meta:
        model = Ride
        fields = (
            'user',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        # self.fields['car'].queryset = Car.objects.filter(user=user)
        self.fields['car'].queryset = user.cars.all()   # related name from Car model


class ReadRideSerializer(serializers.ModelSerializer):
    driver = serializers.SlugRelatedField(slug_field="name", queryset=Driver.objects.all())
    car = serializers.SlugRelatedField(slug_field="plate", queryset=Car.objects.all())
    shift = ShiftSerializer()
    extra_tax = ExtraTaxSerializer()
    user = ReadUserSerializer()

    class Meta:
        model = Ride
        fields = (
            'id',
            'user',
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