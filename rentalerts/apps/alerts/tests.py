
from django.test import TestCase
from django.core import mail
from django.core.management import call_command
from django.contrib.auth.models import User

from rentalerts.apps.apartments.models import Apartment, City, Area
from rentalerts.apps.alerts.models import Search, Alert


class CommandTests(TestCase):

    fixtures = ['auth', 'apartments']

    def _create_search(self, **kwargs):
        user = kwargs.pop('user', None)

        if user is None:
            user = User.objects.create_user("tester2", "tester2@gmail.com", "test")

        return Search.objects.create(user=user, **kwargs)

    def test_create_alerts(self):

        self._create_search(num_rooms=1)
        call_command("create_alerts")

        self.assertEqual(Alert.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 1)

    def test_create_alerts_if_no_email(self):

        self._create_search(num_rooms=1, email=False)
        call_command("create_alerts")

        self.assertEqual(Alert.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 0)
        



class SearchTests(TestCase):

    fixtures = ['auth', 'apartments']

    def _create_search(self, **kwargs):
        user = kwargs.pop('user', None)

        if user is None:
            user = User.objects.create_user("tester2", "tester2@gmail.com", "test")

        return Search.objects.create(user=user, **kwargs)

    def test_create_alerts_no_criteria(self):

        search = self._create_search()

        alerts = search.create_alerts()
        self.assertEqual(len(alerts), 0)

    def test_create_alerts_max_rent(self):

        search = self._create_search(rent_pcm=500)

        alerts = search.create_alerts()
        self.assertEqual(len(alerts), 0)

    def test_create_alerts_non_shared(self):

        search = self._create_search(non_shared=True)

        alerts = search.create_alerts()
        self.assertEqual(len(alerts), 2)

        Apartment.objects.update(is_shared=True)

        alerts = search.create_alerts()
        self.assertEqual(len(alerts), 0)

    def test_create_alerts_num_rooms(self):

        search = self._create_search(num_rooms=1)

        alerts = search.create_alerts()
        self.assertEqual(len(alerts), 2)

    def test_create_alerts_areas(self):

        search = self._create_search()
        search.areas.add(Area.objects.get(name="Soukka"))

        alerts = search.create_alerts()
        self.assertEqual(len(alerts), 1)


    def test_create_alerts_if_same_tenant(self):

        search = self._create_search()
        admin = User.objects.get(username="admin")

        alerts = search.create_alerts()
        self.assertEqual(len(alerts), 0)

    def test_create_alerts_if_already_alert(self):

        search = self._create_search()

        alert = Alert.objects.create(
            user=search.user,
            apartment_id=3,
        )

        alerts = search.create_alerts()
        self.assertEqual(len(alerts), 0)





