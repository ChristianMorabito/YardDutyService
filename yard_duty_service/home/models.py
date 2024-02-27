from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Duty:
	id = models.IntegerField(primary_key=True)
	day = models.CharField(max_length=3)
	start = models.TimeField("start_time")
	end = models.TimeField("end_time")
	location = models.CharField(max_length=30)

	def __str__(self):
		return self.id


class StaffDuty:
	id = models.IntegerField(primary_key=True)
	duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
	staff = models.ForeignKey(User, on_delete=models.CASCADE)
	time_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.id



