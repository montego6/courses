from unittest.mock import Mock
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
import pytest

from courses.blogic import get_user_from_context

@pytest.mark.django_db
def test_get_user_from_context(user):
    request = RequestFactory()
    request.user = user
    context = {'request': request}
    assert get_user_from_context(context) == user

@pytest.mark.parametrize('anon_user', [True, False])
@pytest.mark.django_db
def test_get_user_from_context_none(anon_user):
    request = RequestFactory()
    if anon_user:
        request.user = AnonymousUser()
    context = {'request': request}
    assert get_user_from_context(context) is None