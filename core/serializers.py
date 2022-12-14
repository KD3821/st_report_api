from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Week, Shift, Car, Driver, ExtraTax, Ride, PlanShift
from core.reports import ReportParams



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
        self.fields['car'].queryset = Car.objects.filter(user=user)
        # self.fields['car'].queryset = user.cars.all()   # 'cars' is related name_from Car model
        self.fields['driver'].queryset = user.drivers.all()  # 'drivers' is related_name from Driver model


class ReadRideSerializer(serializers.ModelSerializer):
    driver = serializers.SlugRelatedField(slug_field="name", queryset=Driver.objects.all())
    car = serializers.SlugRelatedField(slug_field="plate", queryset=Car.objects.all())
    shift = ShiftSerializer()
    extra_tax = ExtraTaxSerializer()
    user = ReadUserSerializer()
    # user = UserSerializer()

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


class ReportRidesSerializer(serializers.Serializer):
    shift = ShiftSerializer()
    car = CarSerializer()
    total = serializers.IntegerField()
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParamsSerializer(serializers.Serializer):
    report_date = serializers.DateField()
    report_car = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)


class PlanShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanShift
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"password": "???????????? ???? ??????????????????!"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
