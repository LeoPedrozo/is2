from django.contrib import admin
from .models import Historia
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(Historia,SimpleHistoryAdmin)
