from django.contrib import admin
from .models import Duty, StaffDuty, Year, Holiday, Term


class StaffDutyAdmin(admin.ModelAdmin):
    list_display = ('duty', 'staff', 'custom_info')

    def custom_info(self, obj):
        return obj.time_date.strftime('%H:%M:%S') if obj.time_date else "-"

    custom_info.short_description = 'Sign On Time'


admin.site.register(StaffDuty, StaffDutyAdmin)
admin.site.register(Duty)
admin.site.register(Holiday)
admin.site.register(Term)
admin.site.register(Year)



