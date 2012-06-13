from django.contrib import admin

from rentalerts.apps.apartments.models import Apartment, Area, City


admin.site.register(City)
admin.site.register(Area)
admin.site.register(Apartment)

