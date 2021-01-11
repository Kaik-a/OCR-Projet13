"""Settings used in production"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from . import *

ALLOWED_HOSTS = [
    "178.62.53.45",
    "10.106.0.3",
    "127.0.0.1",
    "gamelenders.site",
    "www.gamelenders.site",
]

DEBUG = False

# SECURITY
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


sentry_sdk.init(
    dsn="https://4c5aa3ff0a1543ac96065ac6d39d7297@o466057.ingest.sentry.io/5581779",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
