from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('rentalerts.apps.home.urls', namespace='home')),
    url(r'^account/', include('rentalerts.apps.accounts.urls', namespace='accounts')),
    url(r'^apartments/', include('rentalerts.apps.apartments.urls', namespace='apartments')),
    url(r'^bookmarks/', include('rentalerts.apps.bookmarks.urls', namespace='bookmarks')),
    url(r'^alerts/', include('rentalerts.apps.alerts.urls', namespace='alerts')),
    url(r'^messages/', include('rentalerts.apps.pm.urls', namespace='pm')),
    #url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
