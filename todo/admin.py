from django.contrib import admin
from .models import Reminder

class ReminderAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)

admin.site.register(Reminder, ReminderAdmin)
