"""
Test configuration for pytest-django. Fixtures put here are apperantly available in all apps
"""

import os
import django
import pytest
import tempfile
import shutil
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model


def pytest_configure():
    """Configure Django settings for pytest"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grumpytracker.settings_test")
    django.setup()


@pytest.fixture
def regular_user():
    """
    Creates an regular user in order to test non-dmin only endpoints
    """
    User = get_user_model()

    return User.objects.create_user(
        username="regular",
        email="regular@test.com",
        password="testpass123",
        is_superuser=False,
        is_staff=False,
    )


@pytest.fixture
def sample_uploaded_file():
    """
    Create a sample uploaded file
    """

    # Create a red square
    image = Image.new("RGB", (100, 100), color="red")
    image_io = BytesIO()
    image.save(image_io, format="PNG")
    image_io.seek(0)

    return SimpleUploadedFile(
        name="test_uploaded_image.png",
        content=image_io.getvalue(),
        content_type="image/png",
    )


@pytest.fixture
def sample_image_file(tmp_path):
    """
    Create a sample image on disk
    """

    # Create a blue square
    image = Image.new("RGB", (100, 100), color="blue")
    image_path = tmp_path / "image_on_disk.png"
    image.save(image_path, format="png")

    return str(image_path)


@pytest.fixture
def single_make():
    """
    Create a single Make in the database
    """
    # We import models inside the fixtures to make sure they are imported only after
    # django is set up
    from makes.models import Make

    return Make.objects.create(name="Sample Make", website="https://www.samplemake.com")


@pytest.fixture
def multiple_makes():
    """
    Create multiple makes on the database
    """
    from makes.models import Make

    makes = [
        Make.objects.create(name="Canon", website="https://www.canon.com"),
        Make.objects.create(name="Sony", website="https://www.sony.com"),
        Make.objects.create(name="Panasonic", website="https://www.panasonic.com"),
    ]

    return makes


@pytest.fixture
def temp_media_dir():
    """
    Create a media directory for testing
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)
