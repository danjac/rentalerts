from rentalerts.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = MANAGERS = (
    ("Danny", "danjac354@gmail.com"),
)

INSTALLED_APPS += ('sentry', 'gunicorn')

# database

DATABASES['default']['NAME'] = ''
DATABASES['default']['USER'] = ''
DATABASES['default']['PASSWORD'] = ""

# static media

STATIC_ROOT = os.path.join(
    os.path.expanduser("~"),
    "webapps", "static"
)

STATIC_URL = "http://static.danjac354.webfactional.com/"
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# email setup

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'rentalerts'
EMAIL_HOST_PASSWORD = 'rentalerts1'
DEFAULT_FROM_EMAIL = 'admin@rentalerts.danjac354.webfactional.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# sentry setup

SENTRY_LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
SENTRY_RUN_DIR= os.path.join(PROJECT_DIR, 'run')
SENTRY_WEB_HOST = '127.0.0.1'
SENTRY_WEB_PORT = 9000
SENTRY_KEY = '%@^tk!eqeaq(bs+nl@(ww6@5cxom!1vcbvqnz^zw26kon7qzdk'

SENTRY_FILTERS = (
    'sentry.filters.StatusFilter',
    'sentry.filters.LoggerFilter',
    'sentry.filters.LevelFilter',
    'sentry.filters.ServerNameFilter',
    'sentry.filters.SiteFilter',
)

SENTRY_VIEWS = (
    'sentry.views.Exception',
    'sentry.views.Message',
    'sentry.views.Query',
)



