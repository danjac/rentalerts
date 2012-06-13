from django.conf.urls import patterns, url

from rentalerts.apps.bookmarks import views

urlpatterns = patterns('',
    url(r'^$', views.BookmarkList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/create/$', views.CreateBookmark.as_view(), name="create"),
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteBookmark.as_view(), name="delete"),
)
