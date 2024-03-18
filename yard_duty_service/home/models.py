from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


class Year(models.Model):
	id = models.AutoField(primary_key=True, null=False)
	current_year = models.IntegerField(unique=True, null=False, default=timezone.now().year, editable=False)

	def __str__(self):
		return str(self.current_year)


class Term(models.Model):

	id = models.AutoField(primary_key=True, null=False)
	number = models.IntegerField(unique=True, null=False, choices=[(1, 1), (2, 2), (3, 3), (4, 4)])
	year = models.ForeignKey(Year, on_delete=models.CASCADE)
	ref_week = models.BooleanField("Week A on ODD week numbers", null=False, default=True)
	start = models.DateField(unique=True, null=False)
	end = models.DateField(unique=True, null=False)

	def __str__(self):
		return f"Term {self.number}\t{self.year}"


class Holiday(models.Model):
	id = models.AutoField(primary_key=True, null=False)
	date = models.DateField(null=True)
	term = models.ForeignKey(Term, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.date)


class Duty(models.Model):
	DAYS_CHOICES = [
		('Mon', 'Monday'),
		('Tue', 'Tuesday'),
		('Wed', 'Wednesday'),
		('Thu', 'Thursday'),
		('Fri', 'Friday'),
	]

	LOCATION_CHOICES = [
		('Admin X-ing', 'Admin Crossing'),
		('MPH X-ing', 'MPH Crossing'),
		('Rear Gate', 'Rear Gate'),
		('Primary A', 'Primary A'),
		('Primary B', 'Primary B'),
		('S. Centre & D Blk', 'Sport Centre & D Block'),
		('MPH & Toilets', 'MPH & Chapel Toilets'),
		('Oval', 'Oval'),
		('Sport Centre', 'Sport Centre w/ Microphone')
	]

	TIME_CHOICES = [
		('8:15 - 8:35', 'Before School 1'),
		('8:35 - 9:00', 'Before School 2'),
		('10:55 - 11:20', 'Recess'),
		('13:00 - 13:25', 'Lunch 1'),
		('13:25 - 13:50', 'Lunch 2'),
		('15:15 - 15:45', 'After School')
	]

	id = models.AutoField(primary_key=True, null=False)
	day = models.CharField(max_length=5, choices=DAYS_CHOICES, null=False)
	start = models.TimeField("Start Time", max_length=4, null=False, editable=False)
	end = models.TimeField("End Time", max_length=4, null=False, editable=False)
	location = models.CharField(max_length=30, choices=LOCATION_CHOICES, null=False)
	preset_times = models.CharField(max_length=30, choices=TIME_CHOICES, null=False)
	term = models.ForeignKey(Term, on_delete=models.CASCADE)
	week = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')], null=False)

	class Meta:
		verbose_name = "Duty"
		verbose_name_plural = 'Duties'
		constraints = [models.UniqueConstraint(fields=['day', 'start', 'end', 'location'], name='Unique constraint')]

	def __str__(self):
		return (f"{self.day}\t"
		        f"{self.start.__str__()[:-3]} - {self.end.__str__()[:-3]}\t "
		        f"{self.location}")

	def save(self, *args, **kwargs):

		if self.preset_times:
			start_time, end_time = self.preset_times.split(' - ')
			start_hour, start_minute = map(int, start_time.split(':'))
			end_hour, end_minute = map(int, end_time.split(':'))
			self.start = datetime.time(start_hour, start_minute)
			self.end = datetime.time(end_hour, end_minute)

		super().save(*args, **kwargs)


class StaffDuty(models.Model):
	id = models.AutoField(primary_key=True, null=False)
	duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
	staff = models.ForeignKey(User, on_delete=models.CASCADE)
	time_date = models.DateTimeField(null=True, editable=False)

	def __str__(self):
		return (f"{self.staff.__str__()}:\t"
		        f"{self.duty.__str__()}")

	def clean(self):
		# Deny staff being 2 places at once (over-lapping times)
		existing_duties = StaffDuty.objects.filter(
			staff=self.staff,
			duty__day=self.duty.day,
			duty__start__lt=self.duty.end,
			duty__end__gt=self.duty.start
		).exclude(pk=self.pk)

		if existing_duties.exists():
			conflicting_duty = existing_duties.first()
			raise ValidationError(f"{self.staff} is already assigned to duty on {conflicting_duty.duty.day} "
			                      f"from {conflicting_duty.duty.start} to {conflicting_duty.duty.end}.")

	class Meta:
		verbose_name = "Assign Staff"
		verbose_name_plural = 'Assign Staff'


# class Status(models.Model):
#
# 	STATUS_CHOICES = [('Today Only', 'Today Only'), ('Custom Range', 'Custom Range'), ('On Going', 'On Going')]
#
# 	id = models.AutoField(primary_key=True, null=False)
# 	status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=False)
# 	start = models.DateField("Start Date", null=False)
# 	end = models.DateField("End Date")


