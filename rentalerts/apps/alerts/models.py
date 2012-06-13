from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from rentalerts.apps.apartments.models import Apartment, Area

class Search(models.Model):
    """
    Search settings for an individual user.
    """

    user = models.OneToOneField(User, primary_key=True)
    email = models.BooleanField("Send email alerts", default=True)

    # search fields

    areas = models.ManyToManyField(Area, blank=True)

    num_rooms = models.IntegerField(
        'Rooms', 
        choices=Apartment.ROOM_CHOICES, 
        null=True, 
        blank=True
    )

    sauna = models.IntegerField(
        choices=Apartment.SAUNA_CHOICES,
        null=True,
        blank=True,
    )


    rent_pcm = models.DecimalField(
        "Max rent/month",
        decimal_places=2,
        max_digits=8,
        null=True,
        blank=True,
    )

    size = models.FloatField("Size (sqm)", null=True, blank=True)

    non_shared = models.BooleanField("Non-shared only", default=False)

    cable = models.BooleanField(default=False)
    broadband = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)

    parking = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)

    pets = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.user)

    def create_alerts(self):

        # don't include my own apartments
        qs = Apartment.objects.exclude(tenant=self.user)

        search = False # ensure we have at least some criteria

        areas = self.areas.all()

        if areas:
            qs = qs.filter(area__in=areas)
            search = True

        if self.num_rooms:
            qs = qs.filter(num_rooms__gte=self.num_rooms)
            search = True

        if self.rent_pcm:
            qs = qs.filter(rent_pcm__lte=self.rent_pcm)
            search = True

        if self.non_shared:
            qs = qs.filter(is_shared=False)
            search = True

        if self.sauna and self.sauna != Apartment.SAUNA_NONE:
            qs = qs.filter(sauna=self.sauna)

        if self.cable:
            qs = qs.filter(cable=True)
            search = True
            
        if self.broadband:
            qs = qs.filter(broadband=True)
            search = True

        if self.balcony:
            qs = qs.filter(balcony=True)
            search = True

        if self.parking:
            qs = qs.filter(parking=True)
            search = True

        if self.laundry:
            qs = qs.filter(laundry=True)
            search = True

        if self.smoking:
            qs = qs.filter(smoking=True)

        if self.pets:
            qs = qs.filter(pets=True)

        if not search:
            return Apartment.objects.none()

        # exclude existing alerts

        apartments = self.user.alert_set.values_list('apartment', flat=True)

        qs = qs.exclude(pk__in=apartments)

        new_alerts = []

        for obj in qs:

            new_alerts.append(Alert(apartment=obj, user=self.user))

        if new_alerts:

            Alert.objects.bulk_create(new_alerts)

        return new_alerts

 
class AlertQuerySet(QuerySet):

    def available(self):
        return self.filter(is_deleted=False)


class AlertManager(models.Manager):

    def get_query_set(self):

        return AlertQuerySet(self.model).select_related(
            'apartment',
            'apartment__area',
            'apartment__area__city',
        )

    def available(self):
        return self.filter(is_deleted=False)



class Alert(models.Model):

    user = models.ForeignKey(User)
    apartment = models.ForeignKey(Apartment)
    created_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    objects = AlertManager()

    class Meta:
        unique_together = ('user', 'apartment')
        ordering = ('-created_on',)



