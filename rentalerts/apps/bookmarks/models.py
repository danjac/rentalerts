from django.db import models
from django.contrib.auth.models import User

from rentalerts.apps.apartments.models import Apartment

class Bookmark(models.Model):

    user = models.ForeignKey(User)
    apartment = models.ForeignKey(Apartment)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)
        unique_together = ('user', 'apartment')

    def __unicode__(self):
        return unicode(self.apartment)

    def get_absolute_url(self):
        return self.apartment.get_absolute_url()
