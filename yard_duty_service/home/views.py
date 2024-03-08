from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from .models import StaffDuty


def get_today():
    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    return weekday_names[(timezone.now() + timezone.timedelta(hours=11)).weekday()]


def is_time_range(obj):
    current_time = timezone.now() + timezone.timedelta(hours=11)
    return obj.duty.start <= current_time.time() < obj.duty.end


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})


def home(request):
    staff_duties_dict = {}
    today = get_today()
    user = request.user
    try:
        staff_duties = list(StaffDuty.objects.filter(staff=user, duty__day=today))
        for sd_instance in staff_duties:
            staff_duties_dict[sd_instance] = is_time_range(sd_instance)

    except ObjectDoesNotExist:
        pass

    context = {'title': 'Home', 'staff_duties': staff_duties_dict}

    return render(request, 'home/home.html', context)


def update_duty(request):
    user = request.user
    today = get_today()
    status = 'not found'

    try:

        staff_duties = list(StaffDuty.objects.filter(staff=user, duty__day=today))
        for sd_instance in staff_duties:
            if is_time_range(sd_instance):
                sd_instance.time_date = timezone.now() + timezone.timedelta(hours=11)
                sd_instance.save()
                status = 'success'
                break

    except ObjectDoesNotExist:
        status = 'fail'

    return JsonResponse({'status': status})
