from django.conf.urls import patterns, url

from rentalerts.apps.apartments import views


urlpatterns = patterns('',
    url(r'^create/$', views.CreateApartment.as_view(), name="create"),
    url(r'^list/$', views.ApartmentList.as_view(), name='list'),
    url(r'^search/$', views.SearchApartments.as_view(), name="search"),
    url(r'^(?P<pk>\d+)/$', views.ApartmentDetail.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/edit/$', views.UpdateApartment.as_view(), name="edit"),
    url(r'^(?P<pk>\d+)/remove/$', views.RemoveApartment.as_view(), name="remove"),
    url(r'^(?P<pk>\d+)/add/$', views.AddApartment.as_view(), name="add"),
)
