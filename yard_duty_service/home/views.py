from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from .models import StaffDuty


WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def current_time_date():
    return timezone.now() + timezone.timedelta(hours=11)


def get_today():
    return WEEKDAYS[current_time_date().weekday()]


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})


def home(request):
    staff_duties = {}
    today = get_today()
    user = request.user
    try:
        sd_list = list(StaffDuty.objects.filter(staff=user, duty__day=today))
        for sd_instance in sd_list:
            staff_duties[sd_instance] = sd_instance.duty.start <= current_time_date().time() < sd_instance.duty.end

    except ObjectDoesNotExist:
        pass

    context = {'title': 'Home', 'staff_duties': staff_duties}

    return render(request, 'home/home.html', context)


def update_duty(request):
    user = request.user
    today = get_today()
    status = 'not found'

    try:

        sd_list = list(StaffDuty.objects.filter(staff=user, duty__day=today))
        for sd_instance in sd_list:
            if sd_instance.duty.start <= current_time_date().time() < sd_instance.duty.end:
                sd_instance.time_date = current_time_date()
                sd_instance.save()
                status = 'success'

    except ObjectDoesNotExist:
        status = 'fail'

    return JsonResponse({'status': status})
