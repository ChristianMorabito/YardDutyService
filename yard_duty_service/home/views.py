from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import StaffDuty, Duty
from django.shortcuts import render
from django.utils import timezone
import json


WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
JSON_CACHE = {}


def update_json_cache():

    curr = None
    for week in Duty._meta.get_field('week').choices:
        for day in Duty._meta.get_field('day').choices:
            for location in Duty._meta.get_field('location').choices:
                for preset_times in Duty._meta.get_field('preset_times').choices:
                    item_list = [week[0], day[0], location[0], f"{preset_times[1]} {preset_times[0]}"]
                    sd_instance = StaffDuty.objects.filter(duty__week=week[0],
                                                           duty__day=day[0],
                                                           duty__location=location[0],
                                                           duty__preset_times=preset_times[0]).first()
                    user = ("Unfilled" if not sd_instance else
                            (sd_instance.staff.__str__() if (sd_instance.staff.first_name == "")
                             else f"{sd_instance.staff.first_name} {sd_instance.staff.last_name}"))

                    # build json
                    for item in item_list:
                        if curr is None:
                            curr = JSON_CACHE

                        if item not in curr:
                            curr[item] = {}
                        curr = curr[item]

                    curr.update({"staff": user, "status": None})
                    curr = None

    with open("test.json", "w") as file:
        file.write(json.dumps(JSON_CACHE))


def current_time_date():
    return timezone.now() + timezone.timedelta(hours=11)


def get_today():
    return WEEKDAYS[current_time_date().weekday()]


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})


def home(request):
    update_json_cache()

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

