from django.conf.urls import patterns, url

from rentalerts.apps.pm import views

urlpatterns = patterns('',
    url(r'^create/(?P<apartment_id>\d+)/$', views.CreateMessage.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.MessageDetail.as_view(), name='detail'),
    url(r'^reply/(?P<parent_id>\d+)/$', views.Reply.as_view(), name='reply'),
    url(r'^received/$', views.ReceivedMessageList.as_view(), name='received_list'),
    url(r'^sent/$', views.SentMessageList.as_view(), name='sent_list'),
)


