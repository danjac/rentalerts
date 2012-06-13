import datetime
import operator

import geopy

from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import permalink
from django.contrib.auth.models import User


geocoder = geopy.geocoders.Google()


class City(models.Model):

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "cities"

    def __unicode__(self):
        return self.name


class Area(models.Model):

    name = models.CharField(max_length=50)
    city = models.ForeignKey(City)

    class Meta:
        unique_together = ('name', 'city')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class ApartmentQuerySet(QuerySet):

    def available(self):

        return self.filter(
            is_available=True,
            tenant__is_active=True,
        )


class ApartmentManager(models.Manager):

    def get_query_set(self):
        return ApartmentQuerySet(self.model).select_related(
                'area', 'area__city')

    def available(self):
        return self.get_query_set().available()

    def search(self, search):

        if search:
            search = search.strip()

        if not search:
            return self.none()

        search_fields = (
            'area__name__iexact',
            'area__city__name__iexact',
            'postcode__iexact',
            'address__icontains',
        )

        criteria = [Q(**{field : search}) 
                        for field in search_fields]

        return self.filter(reduce(operator.or_, criteria))
        

class Apartment(models.Model):

    TYPE_APARTMENT = 1
    TYPE_DETACHED = 2
    TYPE_SEMIDETACHED = 3
    TYPE_COTTAGE =4 

    TYPE_CHOICES = (
        (TYPE_APARTMENT, "Apartment"),
        (TYPE_DETACHED, "Detached house"),
        (TYPE_SEMIDETACHED, "Semi-detached house"),
        (TYPE_COTTAGE, "Cottage"),
    )

    SAUNA_NONE = 1
    SAUNA_SHARED = 2
    SAUNA_OWN = 3

    SAUNA_CHOICES = (
        (SAUNA_NONE, "No sauna"),
        (SAUNA_SHARED, "Shared/communal sauna"),
        (SAUNA_OWN, "Own sauna"),
    )

    ROOM_CHOICES = (
        (1, "1 room"),
        (2, "2 rooms"),
        (3, "3 rooms"),
        (4, "4 rooms"),
    )

    LANDLORD_TENANT = 1
    LANDLORD_PRIVATE = 2
    LANDLORD_AGENCY = 3

    LANDLORD_CHOICES = (
        (LANDLORD_TENANT, "Occupant"),
        (LANDLORD_PRIVATE, "Private landlord"),
        (LANDLORD_AGENCY, "Rental agency"),
    )

    area = models.ForeignKey(Area)
    tenant = models.ForeignKey(User)
    
    landlord = models.IntegerField(
        choices=LANDLORD_CHOICES,
        default=LANDLORD_PRIVATE,
    )

    agency = models.CharField(max_length=100, null=True, blank=True)
    agency_website = models.URLField(null=True, blank=True)

    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=7)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    added_on = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)

    is_shared = models.BooleanField('Shared accomodation', default=False)

    type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=TYPE_APARTMENT,
    )

    num_rooms = models.IntegerField('Rooms', choices=ROOM_CHOICES)
    floor = models.IntegerField(null=True, blank=True)
    lift = models.BooleanField(default=False)
    num_floors = models.IntegerField(null=True, blank=True)

    sauna = models.IntegerField(
        choices=SAUNA_CHOICES,
        default=SAUNA_NONE,
    )

    rent_pcm = models.DecimalField(
        decimal_places=2,
        max_digits=8,
    )

    deposit = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        null=True,
        blank=True
    )

    smoking = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)

    size = models.FloatField('Size (sqm)')
    garden_size = models.FloatField(null=True, blank=True)

    furnished = models.BooleanField(default=False)
    cable = models.BooleanField(default=False)
    broadband = models.BooleanField(default=False)
    satellite = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)

    parking = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)
    bike_storage = models.BooleanField(default=False)
    extra_storage = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)

    description = models.TextField(null=True, blank=True)
    kitchen_amenities = models.TextField(null=True, blank=True)
    furniture = models.TextField(null=True, blank=True)
    heating = models.TextField(null=True, blank=True)
    other_amenities = models.TextField(null=True, blank=True)


    objects = ApartmentManager()


    def __unicode__(self):
        return self.get_full_address()

    @permalink
    def get_absolute_url(self):
        return ('apartments:detail', [str(self.id)])

    def get_full_address(self):

        return "{0}, {1} {2}".format(
            self.address,
            self.postcode,
            self.area.city.name.upper()
        )

    
    def is_agency_landlord(self):
        return self.landlord == self.LANDLORD_AGENCY

    def get_location(self):

        searchable = "{0}, {1} {2}, Finland".format(
            self.address,
            self.postcode,
            self.area.city,
        )

        address, (lat, lng) = geocoder.geocode(
            searchable,
            exactly_one=True
        )

        return lat, lng

    def save(self, *args, **kwargs):
        self.latitude, self.longitude = self.get_location()
        super(Apartment, self).save(*args, **kwargs)

               
