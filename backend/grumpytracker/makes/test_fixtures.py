"""
Shared fixtures for Make tests
"""

import pytest
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.contrib.auth import get_user_model
from makes.models import Make

# Get a user object
User = get_user_model()


@pytest.fixture
def regular_user():
    """
    Creates an regular user in order to test non-dmin only endpoints
    """

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
def make_data():
    """
    Sample data for creating a single Make
    """

    return {"name": "Test Make", "website": "https://www.testmake.com"}


@pytest.fixture
def single_make():
    """
    Create a single Make in the database
    """

    return Make.objects.create(name="Sample Make", website="https://www.samplemake.com")


@pytest.fixture
def multiple_makes():
    """
    Create multiple makes on the database
    """

    makes = [
        Make.objects.create(name="Canon", website="https://www.canon.com"),
        Make.objects.create(name="Sony", website="https://www.sony.com"),
        Make.objects.create(name="Panasonic", website="https://www.panasonic.com"),
    ]

    return makes
