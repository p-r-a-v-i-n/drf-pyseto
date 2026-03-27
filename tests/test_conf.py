import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from drf_pyseto.conf import get_settings


def test_missing_key_raises():
    with override_settings(DRF_PYSETO={}):
        with pytest.raises(ImproperlyConfigured):
            get_settings()
