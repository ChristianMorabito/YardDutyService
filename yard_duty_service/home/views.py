from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from .models import StaffDuty


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})


def home(request):
    return render(request, 'home/home.html')


def update_duty(request):
    user = request.user
    staff_duty_instance = StaffDuty.objects.get(staff=user)

    staff_duty_instance.time_date = timezone.now()
    staff_duty_instance.save()

    return JsonResponse({'status': 'success'})


