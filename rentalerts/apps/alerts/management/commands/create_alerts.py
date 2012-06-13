from django.core.management.base import BaseCommand
from django.template import Context

from rentalerts.apps.helpers.utils.email import send_email_from_template
from rentalerts.apps.alerts.models import Search

class Command(BaseCommand):

    help = "Runs through all user searches and generates alerts"

    def handle(self, *args, **kwargs):

        for search in Search.objects.filter(user__is_active=True):

            alerts = search.create_alerts()

            if alerts and search.email:
                
                send_email_from_template(
                    subject="New alerts",
                    recipient_list=[search.user.email],
                    template="alerts/emails/new_alerts.txt",
                    context=Context({
                        'alerts' : alerts,
                        'user' : search.user,
                    })
                )

