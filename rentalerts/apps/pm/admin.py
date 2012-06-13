from django.contrib import admin

from rentalerts.apps.pm.models import Message

class MessageAdmin(admin.ModelAdmin):

    list_display = (
        'created_on',
        'sender',
        'receiver',
        'subject',
    )

    search_fields = (
        'subject',
        'sender__username',
        'sender__email',
        'receiver__username',
        'receiver__email',
    )

admin.site.register(Message, MessageAdmin)
