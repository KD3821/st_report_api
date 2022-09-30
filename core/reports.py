import datetime
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from core.models import Ride, Shift, Car
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ReportRides:
    shift: Shift
    car: Car
    total: int
    count: int
    avg: Decimal

@dataclass
class ReportParams:
    report_date: datetime.date
    report_car: str
    user: User

def rides_report(params: ReportParams):
    data = []
    queryset = Ride.objects.select_related(
        "car",
        "shift"
    ).filter(
        user=params.user,
        shift__date=params.report_date,
        car__plate=params.report_car
    ).values("shift", "car").annotate(
        total=Sum("price"),
        count=Count("id"),
        avg=Avg("price")
    )

    shift = Shift.objects.filter(date=params.report_date)[0:1].get()
    car = Car.objects.filter(plate=params.report_car)[0:1].get()

    for ride in queryset:
        reporting_rides = ReportRides(shift, car, ride["total"], ride["count"], ride["avg"])
        data.append(reporting_rides)

    return data