from django.contrib import admin
from .models import Duty, StaffDuty


class StaffDutyAdmin(admin.ModelAdmin):
    list_display = ('duty', 'staff', 'custom_info')

    def custom_info(self, obj):
        return f"{obj.time_date.strftime('%H:%M:%S')}"

    custom_info.short_description = 'Sign On Time'


admin.site.register(StaffDuty, StaffDutyAdmin)
admin.site.register(Duty)


