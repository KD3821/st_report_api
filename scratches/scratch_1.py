from rest_framework import serializers
from datetime import date

class PersonSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    birthdate = serializers.DateField()
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        delta = date.today() - obj.birthdate
        return int(delta.days / 365)

    def validate_birthdate(self, value):
        if value > date.today():
            raise serializers.ValidationError("The birthdate must be a date before or today")
        return value

    def validate(self, data):
        if not data["first_name"] and not data["last_name"]:
            raise serializers.ValidationError("You must enter at least either first or last name")
        return data

    def save(self, **kwargs):
        pass

class Person:
    def __init__(self, first_name, last_name, birthdate):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
