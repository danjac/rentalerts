from django.contrib.auth import decorators as auth

from rentalerts.apps.helpers.decorators import make_view_decorator

login_required = make_view_decorator(auth.login_required)






