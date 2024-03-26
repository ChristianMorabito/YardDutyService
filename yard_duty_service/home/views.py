from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import StaffDuty, Duty, User
from django.shortcuts import render
from django.utils import timezone
import json
import os

UNFILLED_STRING = "Unfilled"
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
JSON_FILE_PATH = 'home/static/home/data.json'
JSON_CACHE = {}


def get_user_string(user):
    return user.__str__() if (user.first_name == "") else f"{user.first_name} {user.last_name}"


def create_json(request):
    # unfilled string is part of the staff list
    staff_list = [UNFILLED_STRING] + [get_user_string(curr_user) for curr_user in User.objects.filter()]

    JSON_CACHE.update({
        "staffList": staff_list,
        "titleTop": [], "titleSide": [], "week": {}})

    for week, _ in Duty._meta.get_field('week').choices:
        if week not in JSON_CACHE["week"]:
            JSON_CACHE["week"][week] = {}

        for day, _ in Duty._meta.get_field('day').choices:
            if day not in JSON_CACHE["week"][week]:
                JSON_CACHE["week"][week][day] = []

            for time, _ in Duty._meta.get_field('preset_times').choices:
                # fill the titleSide array just once.
                if len(JSON_CACHE["titleSide"]) < len(Duty._meta.get_field('preset_times').choices):
                    JSON_CACHE["titleSide"].append(time)

                row_data = []

                for location, _ in Duty._meta.get_field('location').choices:
                    # fill the titleTop array just once.
                    if len(JSON_CACHE["titleTop"]) < len(Duty._meta.get_field('location').choices):
                        JSON_CACHE["titleTop"].append(location)

                    sd_instance = StaffDuty.objects.filter(duty__week=week,
                                                           duty__day=day,
                                                           duty__location=location,
                                                           duty__preset_times=time).first()

                    user = (UNFILLED_STRING if not sd_instance else
                            (sd_instance.staff.__str__() if (sd_instance.staff.first_name == "")
                             else f"{sd_instance.staff.first_name} {sd_instance.staff.last_name}"))

                    row_data.append(user)
                JSON_CACHE["week"][week][day].append(row_data)

    with open(JSON_FILE_PATH, "w") as file:
        file.write(json.dumps(JSON_CACHE))


def load_json(request):

    if not os.path.exists(JSON_FILE_PATH) or os.path.getsize(JSON_FILE_PATH) == 0:
        create_json(request)

    # TODO: don't forget to UPDATE json too.
    with open(JSON_FILE_PATH) as json_file:
        data = json.load(json_file)
    return JsonResponse(data)


def current_time_date():
    return timezone.now() + timezone.timedelta(hours=11)


def get_today():
    return WEEKDAYS[current_time_date().weekday()]


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})


@login_required(login_url='/users/login')
def home(request):
    load_json(request)

    staff_duties = {}
    today = get_today()
    user = request.user
    try:
        sd_list = list(StaffDuty.objects.filter(staff=user, duty__day=today))
        for sd_instance in sd_list:
            staff_duties[sd_instance.duty] = sd_instance.duty.start <= current_time_date().time() < sd_instance.duty.end

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


@login_required(login_url='/users/login')
def get_username(request):
    user_data = {
        "name": (request.user.__str__()
                 if (request.user.first_name == "") else f"{request.user.first_name} {request.user.last_name}"),
        "admin": request.user.is_superuser
    }

    return JsonResponse(user_data)
