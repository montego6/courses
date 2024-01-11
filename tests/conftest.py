import pytest
from django.conf import settings

@pytest.fixture(autouse=True)
def disable_logging():
    print('Fixture')
    settings.MIDDLEWARE.remove('loggers.middlewares.LogRequestsMiddleware')