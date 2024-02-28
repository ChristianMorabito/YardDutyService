from django.db import models
from django.contrib.auth.models import User


class Duty(models.Model):
	DAYS_CHOICES = [
		('Mon', 'Monday'),
		('Tue', 'Tuesday'),
		('Wed', 'Wednesday'),
		('Thu', 'Thursday'),
		('Fri', 'Friday'),
	]

	id = models.AutoField(primary_key=True, null=False)
	day = models.CharField(max_length=3, choices=DAYS_CHOICES, null=False)
	start = models.TimeField("Start Time", null=False, max_length=4)
	end = models.TimeField("End Time", null=False)
	location = models.CharField(max_length=30, null=False)

	class Meta:
		verbose_name = "Set Duty Time"
		verbose_name_plural = 'Set Duty Times'

	def __str__(self):
		return (f"{self.day}\t"
		        f"{self.start.__str__()[:-3]}-{self.end.__str__()[:-3]}\t "
		        f"{self.location}")


class StaffDuty(models.Model):
	id = models.AutoField(primary_key=True, null=False)
	duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
	staff = models.ForeignKey(User, on_delete=models.CASCADE)
	time_date = models.DateTimeField(null=True, editable=False)

	class Meta:
		verbose_name = "Assign Staff to Duty"
		verbose_name_plural = 'Assign Staff to Duties'



