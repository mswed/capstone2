"""
Test configuration for pytest-django
"""

import os
import django


def pytest_configure():
    """Configure Django settings for pytest"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grumpytracker.settings_test")
    django.setup()
