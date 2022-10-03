from django.db import models
from django.contrib.auth.models import User
from django.db.models import DateField, CharField, IntegerField, BooleanField, ForeignKey, TextField



class Week(models.Model):
    week = IntegerField(default=1)

    def __str__(self):
        return f'{self.week}'



class Shift(models.Model):
    date = DateField()
    week = ForeignKey(Week, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.date}'



class Car(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    plate = CharField(max_length=200)
    rental_rate = IntegerField(default=3000)

    def __str__(self):
        return self.plate



class Driver(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='drivers')
    name = CharField(max_length=200)
    salary = IntegerField(default=0)
    tips = IntegerField(default=0)
    costs = IntegerField(default=0)
    deposit = IntegerField(default=0)
    fines = IntegerField(default=0)

    def __str__(self):
        return self.name



class ExtraTax(models.Model):
    mode = CharField(max_length=100)
    tax = IntegerField(default=0)

    def __str__(self):
        return self.mode



class Ride(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    number = CharField(max_length=50, verbose_name='Номер заказа')
    driver = ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='Водитель')
    car = ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Авто')
    shift = ForeignKey(Shift, on_delete=models.CASCADE, verbose_name='День')
    price = IntegerField(default=0, verbose_name='Стоимость')
    tip = IntegerField(default=0, verbose_name='Чаевые')
    cash = BooleanField(default=False, verbose_name='За наличные')
    toll = IntegerField(default=0, verbose_name='ЗСД')
    save_tax = BooleanField(default=False, verbose_name='С покупкой смены')
    saved_tax_result = IntegerField(default=0, verbose_name='Экономия комиссии')
    extra_tax = ForeignKey(ExtraTax, on_delete=models.CASCADE, verbose_name='Режим доп.комиссии')
    tax_result = IntegerField(default=0, verbose_name='Сумма доп.комиссии')
    comment = TextField(max_length=200, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.number



class PlanShift(models.Model):
    plan_day = ForeignKey(Shift, on_delete=models.CASCADE)
    plan_car = ForeignKey(Car, on_delete=models.CASCADE)
    plan_driver = ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.plan_day}-{self.plan_car}'


class AllowList(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address