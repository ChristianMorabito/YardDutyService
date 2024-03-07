from django.contrib import admin
from .models import Duty, StaffDuty
from datetime import timezone, timedelta


class StaffDutyAdmin(admin.ModelAdmin):
    list_display = ('duty', 'staff', 'custom_info')

    def custom_info(self, obj):
        if obj.time_date:
            new_timezone = timezone(timedelta(hours=11))  # UTC+11 (Australia/Melbourne)
            time_in_new_timezone = obj.time_date.astimezone(new_timezone)
            return f"{time_in_new_timezone.strftime('%H:%M:%S')}"
        else:
            return "-"

    custom_info.short_description = 'Sign On Time'


admin.site.register(StaffDuty, StaffDutyAdmin)
admin.site.register(Duty)


