import mock

from django.test import TestCase
from django.contrib.auth.models import User

from rentalerts.apps.apartments.models import Apartment, City, Area


class MockApartment(object):

    @classmethod
    def get_location(cls):

        return (0.3456, 0.12345)


class ApartmentTests(TestCase):

    @mock.patch.object(
        Apartment, 
        'get_location', 
        MockApartment.get_location
    )
    def _create_apartment(self, **kwargs):

        user = kwargs.pop('user', None)
        city = kwargs.pop('city', None)
        area = kwargs.pop('area', None)

        if user is None:
            user = User.objects.create_user("tester", "tester@gmail.com", "test")

        if city is None:
            city = City.objects.create(name="Espoo")

        if area is None:
            area  = Area.objects.create(name="Soukka", city=city)
 
        values = dict(
            address="Kastevuorenkuja 3 K163",
            postcode="12360",
            area=area,
            tenant=user,
            sauna=Apartment.SAUNA_NONE,
            rent_pcm=1000,
            size=20,
            num_rooms=1,
        )

        values.update(kwargs)

        return Apartment.objects.create(**values)

    def test_available_if_available(self):

        apt = self._create_apartment()

        apts = Apartment.objects.all().available()
        self.assertEqual(apts.count(), 1)

        apts = Apartment.objects.available()
        self.assertEqual(apts.count(), 1)

    def test_available_if_not_available(self):

        apt = self._create_apartment(is_available=False)

        apts = Apartment.objects.all().available()
        self.assertEqual(apts.count(), 0)

        apts = Apartment.objects.available()
        self.assertEqual(apts.count(), 0)

    def test_search_if_empty(self):

        apt = self._create_apartment()

        apts = Apartment.objects.search(None)
        self.assertEqual(apts.count(), 0)

        apts = Apartment.objects.search('')
        self.assertEqual(apts.count(), 0)

        apts = Apartment.objects.search('  ')
        self.assertEqual(apts.count(), 0)

    def test_search_if_wrong(self):

        apt = self._create_apartment()

        apts = Apartment.objects.search('00777')
        self.assertEqual(apts.count(), 0)

    def test_search_if_right(self):

        apt = self._create_apartment()

        apts = Apartment.objects.search('12360')
        self.assertEqual(apts.count(), 1)

        apts = Apartment.objects.search('espoo')
        self.assertEqual(apts.count(), 1)

 
    def test_save_location(self):
        """
        Test lat/lng updated with each save
        """

        apt = self._create_apartment()
        self.assertEqual(apt.latitude, 0.3456)
        self.assertEqual(apt.longitude, 0.12345)
