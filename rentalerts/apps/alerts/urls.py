from django.conf.urls import patterns, url

from rentalerts.apps.alerts import views

urlpatterns = patterns('',
    url(r'^$', views.AlertList.as_view(), name="list"),
    url(r'^edit/$', views.EditSearch.as_view(), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteAlert.as_view(), name='delete'),
)
   
