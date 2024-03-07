from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timezone, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from .models import StaffDuty


def get_current_time():
    current_time_utc = datetime.now(timezone.utc)
    new_timezone = timezone(timedelta(hours=11))
    return current_time_utc.astimezone(new_timezone)


def get_today():
    day_of_week = get_current_time().weekday()
    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    return weekday_names[day_of_week]


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})


def home(request):

    staff_duties = []
    today = get_today()
    user = request.user
    try:
        staff_duties.append(StaffDuty.objects.get(staff=user, duty__day=today))
    except ObjectDoesNotExist:
        pass

    context = {'title': 'Home', 'staff_duties': staff_duties}

    return render(request, 'home/home.html', context)


def update_duty(request):
    user = request.user
    today = get_today()
    status = 'success'

    try:
        staff_duty_instance = StaffDuty.objects.get(staff=user, duty__day=today)
        staff_duty_instance.time_date = get_current_time()
        staff_duty_instance.save()

    except ObjectDoesNotExist:
        status = 'not_found'

    return JsonResponse({'status': status})
