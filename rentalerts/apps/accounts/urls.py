from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from rentalerts.apps.accounts import views, forms

urlpatterns = patterns('',
    url(r'^settings/$', views.Settings.as_view(), name='settings'),
    url(r'^change/$', views.AccountSettings.as_view(), name='account_settings'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^register-success/$', views.RegisterSuccess.as_view(), name='register_success'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
)


# password change/reset views

urlpatterns += patterns('django.contrib.auth.views',

    url(r'^password_change/$', 'password_change', {
           'post_change_redirect' : reverse_lazy('accounts:password_change_done'),  
           'password_change_form' : forms.PasswordChangeForm,
           'template_name' : 'accounts/password_change_form.html',
        }, name='password_change'),

    url(r'^password_change/done/$', 'password_change_done', {
            'template_name' : 'accounts/password_change_done.html', 
        }, name='password_change_done'),

    url(r'^password_reset/$', 'password_reset', {
            'post_reset_redirect' : reverse_lazy('accounts:password_reset_done'),
            'template_name' : 'accounts/password_reset_form.html',
            'email_template_name' : 'accounts/email/password_reset.txt',
            'password_reset_form' : forms.PasswordResetForm,
        }, name='password_reset'),

    url(r'^password_reset/done/$', 'password_reset_done', {
            'template_name' :  'accounts/password_reset_done.html',
        },  name='password_reset_done'),


    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm', {
            'post_reset_redirect' : reverse_lazy('accounts:password_reset_complete'),
            'set_password_form' : forms.SetPasswordForm,
            'template_name' : 'accounts/reset_password_confirm.html',
         },name='password_reset_confirm'),

    url(r'^reset/done/$', 'password_reset_complete', {
            'template_name' : 'accounts/password_reset_complete.html', 
        }, name='password_reset_complete'),
)
