from rentalerts.settings.base import *

DATABASES['default']['NAME'] = 'rentalerts_development'
DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = 'm0nk3Y'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CRISPY_FAIL_SILENTLY = False

