from cameras.models import CameraManufacturer, Camera, Format, Source
from django.db import transaction
from loguru import logger


@transaction.atomic
def clear_database():
    formats_count = Format.objects.count()
    Format.objects.all().delete()

    sources_count = Source.objects.count()
    Source.objects.all().delete()

    cameras_count = Camera.objects.count()
    Camera.objects.all().delete()

    manufacturers_count = CameraManufacturer.objects.count()
    CameraManufacturer.objects.all().delete()

    logger.info(f"Deleted {manufacturers_count} manufacturers")
    logger.info(f"Deleted {cameras_count} cameras")
    logger.info(f"Deleted {sources_count} sources")
    logger.info(f"Deleted {formats_count} formats")


@transaction.atomic
def seed_manufacturers():
    manufacturers = [
        {"name": "Arri", "website": "https://www.arri.com/en"},
        {"name": "RED", "website": "https://www.red.com"},
    ]

    created_manufacturers = {}
    for mfg in manufacturers:
        manufacturer, new = CameraManufacturer.objects.get_or_create(**mfg)
        created_manufacturers[mfg["name"]] = manufacturer
        logger.info(
            f"{'Created' if new else 'Found'} manufacturer: {manufacturer.name}"
        )

    return created_manufacturers


@transaction.atomic
def seed_cameras(manufacturers):
    cameras = [
        {
            "manufacturer": manufacturers.get("Arri")
            or CameraManufacturer.objects.get("Arri"),
            "model": "Alexa 35",
            "sensor_type": "Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array",
            "max_filmback_width": 27.99,
            "max_filmback_height": 19.22,
            "max_image_width": 4608,
            "max_image_height": 3164,
            "min_frame_rate": 0.75,
            "max_frame_rate": 120,
        }
    ]

    created_cameras = {}
    for cam in cameras:
        camera, new = Camera.objects.get_or_create(**cam)
        created_cameras[cam["model"]] = camera
        logger.info(f"{'Created' if new else 'Found'} camera: {camera.model}")

    return created_cameras


@transaction.atomic
def seed_sources():
    sources = [
        {
            "name": "Alexa 35 User Manual",
            "url": "https://www.arri.com/resource/blob/389818/03a1421ba039d246cd4c895c2f791f79/alexa-35-user-manual-sup-4-0-0-data.pdf",
        }
    ]

    created_sources = {}
    for s in sources:
        source, new = Source.objects.get_or_create(**s)
        created_sources[s["name"]] = source
        logger.info(f"{'Created' if new else 'Found'} source`: {source.name}")

    return created_sources


@transaction.atomic
def seed_formats(cameras, sources):
    formats = [
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4.6K",
            "image_aspect": "3:2",
            "format_name": "Open Gate",
            "sensor_width": 28.0,
            "sensor_height": 19.2,
            "image_width": 4608,
            "image_height": 3164,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa 35 User Manual"),
        }
    ]

    created_formats = {}
    for fmt in formats:
        format_record, new = Format.objects.get_or_create(**fmt)
        created_formats[format_record.id] = format_record
        logger.info(
            f"{'Created' if new else 'Found'} format: {format_record.image_format} {format_record.image_aspect} {format_record.format_name} {format_record.codec}"
        )


def seed_db():
    clear_database()
    manufacturers = seed_manufacturers()
    cameras = seed_cameras(manufacturers)
    sources = seed_sources()
    formats = seed_formats(cameras, sources)
