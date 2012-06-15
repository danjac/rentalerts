from django.conf.urls import patterns, url


from rentalerts.apps.home import views

urlpatterns = patterns('',
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^about/$', views.AboutPage.as_view(), name="about"),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
)
