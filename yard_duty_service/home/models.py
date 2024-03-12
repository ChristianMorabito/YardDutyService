from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Duty(models.Model):
	DAYS_CHOICES = [
		('Mon', 'Monday'),
		('Tue', 'Tuesday'),
		('Wed', 'Wednesday'),
		('Thu', 'Thursday'),
		('Fri', 'Friday'),
	]

	id = models.AutoField(primary_key=True, null=False)
	day = models.CharField(max_length=5, choices=DAYS_CHOICES, null=False)
	start = models.TimeField("Start Time", max_length=4)
	end = models.TimeField("End Time")
	location = models.CharField(max_length=30, null=False)

	class Meta:
		verbose_name = "Duty"
		verbose_name_plural = 'Duties'
		constraints = [models.UniqueConstraint(fields=['day', 'start', 'end', 'location'], name='Unique constraint')]

	def __str__(self):
		return (f"{self.day}\t"
		        f"{self.start.__str__()[:-3]}-{self.end.__str__()[:-3]}\t "
		        f"{self.location}")


class StaffDuty(models.Model):
	id = models.AutoField(primary_key=True, null=False)
	duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
	staff = models.ForeignKey(User, on_delete=models.CASCADE)
	time_date = models.DateTimeField(null=True, editable=False)

	def __str__(self):
		return (f"{self.staff.__str__()}:\t"
		        f"{self.duty.__str__()}")

	def clean(self):
		# Check if there is any existing duty assigned to the same staff on the same day and within the same time range
		existing_duties = StaffDuty.objects.filter(
			staff=self.staff,
			duty__day=self.duty.day,
			duty__start__lt=self.duty.end,
			duty__end__gt=self.duty.start
		).exclude(pk=self.pk)  # Exclude the current instance if it's being updated

		if existing_duties.exists():
			conflicting_duty = existing_duties.first()
			raise ValidationError(f"{self.staff} is already assigned to duty on {conflicting_duty.duty.day} "
			                      f"from {conflicting_duty.duty.start} to {conflicting_duty.duty.end}.")

	class Meta:
		verbose_name = "Assign Staff"
		verbose_name_plural = 'Assign Staff'








