from django.contrib import admin

from rentalerts.apps.alerts.models import Alert


class AlertAdmin(admin.ModelAdmin):

    list_display = ('apartment', 'user', 'is_deleted')
    list_editable = ('is_deleted',) 

admin.site.register(Alert, AlertAdmin)
