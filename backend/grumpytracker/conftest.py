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
    Create multiple makes in the database
    """
    from makes.models import Make

    makes = [
        Make.objects.create(name="Canon", website="https://www.canon.com"),
        Make.objects.create(name="Sony", website="https://www.sony.com"),
        Make.objects.create(name="Panasonic", website="https://www.panasonic.com"),
    ]

    return makes


@pytest.fixture
def single_camera(db):
    """
    Create a single Make in the database
    """
    # We import models inside the fixtures to make sure they are imported only after
    # django is set up
    from makes.models import Make
    from cameras.models import Camera

    make = Make.objects.create(name="RED", website="https://www.red.com")

    return Camera.objects.create(
        make=make,
        model="KOMODO",
        sensor_type="KOMODO® 19.9 MP Super 35mm Global Shutter CMOS",
        sensor_size="Super 35",
        max_filmback_width=27.03,
        max_filmback_height=14.26,
        max_image_width=6144,
        max_image_height=3240,
        min_frame_rate=24,
        max_frame_rate=120,
    )


@pytest.fixture
def multiple_cameras(db):
    """
    Create multiple cameras in the database
    :param db: database markup for this function so it can be run by multiple formats
    """
    from makes.models import Make
    from cameras.models import Camera

    makes = [
        Make.objects.create(name="Arri", website="https://www.arri.com"),
        Make.objects.create(name="RED", website="https://www.red.com"),
    ]
    cameras_data = [
        {
            "make": makes[0],
            "model": "Alexa 35",
            "sensor_type": "Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            "sensor_size": "Super 35",
            "max_filmback_width": 27.99,
            "max_filmback_height": 19.22,
            "max_image_width": 4608,
            "max_image_height": 3164,
            "min_frame_rate": 0.75,
            "max_frame_rate": 120,
        },
        {
            "make": makes[0],
            "model": "Alexa Mini LF",
            "sensor_type": "Large Format ARRI ALEV III (A2X) CMOS sensor with Bayer pattern color filter array",
            "sensor_size": "Large Format",
            "max_filmback_width": 36.70,
            "max_filmback_height": 25.54,
            "max_image_width": 4448,
            "max_image_height": 3096,
            "min_frame_rate": 0.75,
            "max_frame_rate": 90,
            "image": "arri_alexa_mini.png",
        },
        {
            "make": makes[1],
            "model": "KOMODO",
            "sensor_type": "KOMODO® 19.9 MP Super 35mm Global Shutter CMOS",
            "sensor_size": "Super 35",
            "max_filmback_width": 27.03,
            "max_filmback_height": 14.26,
            "max_image_width": 6144,
            "max_image_height": 3240,
            "min_frame_rate": 24,
            "max_frame_rate": 120,
        },
        {
            "make": makes[1],
            "model": "KOMODO-X",
            "sensor_type": "KOMODO-X™ 19.9MP Super 35mm Global Shutter CMOS",
            "sensor_size": "Super 35",
            "max_filmback_width": 27.03,
            "max_filmback_height": 14.26,
            "max_image_width": 6144,
            "max_image_height": 3240,
            "min_frame_rate": 24,
            "max_frame_rate": 240,
        },
    ]

    cameras = [Camera.objects.create(**cam) for cam in cameras_data]

    return cameras


@pytest.fixture
def single_source(db):
    """
    Create a single Source in the database
    :param db: database markup for this function so it can be run by multiple formats
    """
    # We import models inside the fixtures to make sure they are imported only after
    # django is set up
    from sources.models import Source

    return Source.objects.create(
        name="Sample Source",
        url="https://www.samplesource.com",
        file_name="file_on_disk.pdf",
        note="Nothing to see here",
    )


@pytest.fixture
def multiple_sources():
    """
    Create multiple sources in the database
    """
    from sources.models import Source

    makes = [
        Source.objects.create(
            name="Source-A",
            url="https://www.example_a.net",
            file_name="source_a.pdf",
            note="source A note",
        ),
        Source.objects.create(
            name="Source-B",
            url="https://www.example_b.net",
            file_name="source_b.pdf",
            note="source B note",
        ),
        Source.objects.create(
            name="Source-C",
            url="https://www.example_c.org",
            file_name="source_c.pdf",
            note="source C note",
        ),
        Source.objects.create(
            name="Source-CD",
            url="https://www.example_d.dev",
            file_name="source_cd.pdf",
            note="source CD note",
        ),
    ]

    return makes


@pytest.fixture
def single_format(single_camera, single_source):
    """
    Create a single format in the database
    """
    # We import models inside the fixtures to make sure they are imported only after
    # django is set up
    from formats.models import Format

    camera = single_camera
    source = single_source

    return Format.objects.create(
        camera=camera,
        image_format="HD",
        image_aspect="16:9",
        format_name="S16",
        sensor_width=13.20,
        sensor_height=7.43,
        image_width=1920,
        image_height=1080,
        codec="ProRes",
        source=source,
        make_notes="Records images in 1920x1080 resolution. Uses a 1600x900 sensor center crop and scales it to 1920x1080.",
    )


@pytest.fixture
@pytest.mark.django_db
def multiple_formats(multiple_cameras, single_source):
    """
    Create multiple formats in the database
    """
    from formats.models import Format

    cameras = multiple_cameras
    source = single_source

    formats_data = [
        {
            "camera": cameras[0],
            "image_format": "4.6K",
            "image_aspect": "3:2",
            "format_name": "Open Gate",
            "sensor_width": 28.0,
            "sensor_height": 19.2,
            "image_width": 4608,
            "image_height": 3164,
            "codec": "ARRIRAW",
            "source": source,
            "make_notes": "4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
            "is_downsampled": True,
        },
        {
            "camera": cameras[0],
            "image_format": "3K",
            "image_aspect": "3:2",
            "format_name": "Open Gate",
            "sensor_width": 28.0,
            "sensor_height": 19.2,
            "image_width": 4608,
            "image_height": 3164,
            "codec": "ProRes",
            "source": source,
            "make_notes": "4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
            "is_upscaled": True,
        },
        {
            "camera": cameras[-1],
            "image_format": "4K",
            "image_aspect": "16:9",
            "sensor_width": 16.90,
            "sensor_height": 9.50,
            "image_width": 3840,
            "image_height": 2160,
            "codec": "R3D",
            "source": source,
            "raw_recording_available": False,
            "notes": "A sample note",
        },
        {
            "camera": cameras[-1],
            "image_format": "2K",
            "image_aspect": "17:9",
            "sensor_width": 9.01,
            "sensor_height": 4.75,
            "image_width": 2048,
            "image_height": 1080,
            "is_anamorphic": True,
            "is_desqueezed": True,
            "pixel_aspect": 2.0,
            "codec": "R3D",
            "source": source,
        },
    ]

    formats = [Format.objects.create(**fmt) for fmt in formats_data]

    return formats


@pytest.fixture
def temp_media_dir():
    """
    Create a media directory for testing
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)
