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
        },
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
            "manufacturer_notes": "4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4.6K",
            "image_aspect": "3:2",
            "format_name": "Open Gate",
            "sensor_width": 28.0,
            "sensor_height": 19.2,
            "image_width": 4608,
            "image_height": 3164,
            "codec": "ProRes",
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4.6K",
            "image_aspect": "16:9",
            "sensor_width": 28.0,
            "sensor_height": 15.7,
            "image_width": 4608,
            "image_height": 2592,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "Full sensor width recording in a 16:9 format that suits many spherical Super 35 and all large format lenses, with room for flexibility in post. Lower data rate than 4.6K 3.2 Open Gate.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4K",
            "image_aspect": "16:9",
            "sensor_width": 28.0,
            "sensor_height": 15.7,
            "image_width": 4096,
            "image_height": 2304,
            "is_downsampled": True,
            "codec": "ProRes",
            "source": sources.get("Alexa 35 User Manual"),
            "notes": "Downsampled from 4.6K 16:9",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4K",
            "image_aspect": "16:9",
            "sensor_width": 24.9,
            "sensor_height": 14,
            "image_width": 4096,
            "image_height": 2304,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "4K 16:9 mimics the traditional spherical Super 35 film format for maximum lens compatibility. Multiple in-camera downsampling options provide lower data rates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4K",
            "image_aspect": "16:9",
            "sensor_width": 24.9,
            "sensor_height": 14,
            "image_width": 4096,
            "image_height": 2304,
            "codec": "ProRes",
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "4K 16:9 mimics the traditional spherical Super 35 film format for maximum lens compatibility. Multiple in-camera downsampling options provide lower data rates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "UHD",
            "sensor_width": 24.9,
            "sensor_height": 14,
            "image_width": 3840,
            "image_height": 2160,
            "codec": "ProRes",
            "is_downsampled": True,
            "source": sources.get("Alexa 35 User Manual"),
            "notes": "Downsampled from 4K 16:9",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "2K",
            "sensor_width": 24.9,
            "sensor_height": 14,
            "image_width": 2048,
            "image_height": 1152,
            "codec": "ProRes",
            "is_downsampled": True,
            "source": sources.get("Alexa 35 User Manual"),
            "notes": "Downsampled from 4K 16:9",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "HD",
            "sensor_width": 24.9,
            "sensor_height": 14,
            "image_width": 2048,
            "image_height": 1152,
            "codec": "ProRes",
            "is_downsampled": True,
            "source": sources.get("Alexa 35 User Manual"),
            "notes": "Downsampled from 4K 16:9",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4K",
            "image_aspect": "2:1",
            "sensor_width": 24.9,
            "sensor_height": 12.4,
            "image_width": 4096,
            "image_height": 2048,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa 35 User Manual"),
            "notes": "Downsampled from 4K 16:9",
            "manufacturer_notes": "4K 2:1 was designed for shooting with all spherical Super 35 and large format lenses for a target deliverable of 2:1, fulfilling 4K mandates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4K",
            "image_aspect": "2:1",
            "sensor_width": 24.9,
            "sensor_height": 12.4,
            "image_width": 4096,
            "image_height": 2048,
            "codec": "ProRes",
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "4K 2:1 was designed for shooting with all spherical Super 35 and large format lenses for a target deliverable of 2:1, fulfilling 4K mandates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "3.8K",
            "image_aspect": "16:9",
            "sensor_width": 23.3,
            "sensor_height": 13.1,
            "image_width": 3840,
            "image_height": 2160,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "For projects using spherical lenses for a 16:9 UHD deliverable. Smaller sensor area than sensor mode `4.6K 16:9` ennsures that most S35 format lenses cover. Lower data rate and higher fps than sensor modes ‘4.6K 3:2 Open Gate’ and ‘4.6K 16:9’.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "3.8K",
            "image_aspect": "16:9",
            "sensor_width": 23.3,
            "sensor_height": 13.1,
            "image_width": 3840,
            "image_height": 2160,
            "codec": "ProRes",
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "For projects using spherical lenses for a 16:9 UHD deliverable. Smaller sensor area than sensor mode `4.6K 16:9` ennsures that most S35 format lenses cover. Lower data rate and higher fps than sensor modes ‘4.6K 3:2 Open Gate’ and ‘4.6K 16:9’.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "3.3K",
            "image_aspect": "6:5",
            "sensor_width": 20.2,
            "sensor_height": 16.9,
            "image_width": 3328,
            "image_height": 2790,
            "codec": "ARRIRAW",
            "is_anamorphic": True,
            "pixel_aspect": 2.0,
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "For projects using 2x anamorphic Super 35 lenses for a target deliverable of 2.39:1. Negates necessity of cropping 4:3 footage and fulfills 4K mandates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "3.3K",
            "image_aspect": "6:5",
            "sensor_width": 20.2,
            "sensor_height": 16.9,
            "image_width": 3328,
            "image_height": 2790,
            "codec": "ProRes",
            "is_anamorphic": True,
            "pixel_aspect": 2.0,
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "For projects using 2x anamorphic Super 35 lenses for a target deliverable of 2.39:1. Negates necessity of cropping 4:3 footage and fulfills 4K mandates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "4K",
            "image_aspect": "2.39:1",
            "format_name": "Ana. 2X",
            "sensor_width": 20.2,
            "sensor_height": 16.9,
            "image_width": 4096,
            "image_height": 1716,
            "codec": "ProRes",
            "is_anamorphic": True,
            "is_desqueezed": True,
            "pixel_aspect": 2.0,
            "source": sources.get("Alexa 35 User Manual"),
            "notes": "Dezqueezed from 3.3K 6:5",
            "manufacturer_notes": "For projects using 2x anamorphic Super 35 lenses for a target deliverable of 2.39:1. Negates necessity of cropping 4:3 footage and fulfills 4K mandates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "3K",
            "image_aspect": "1:1",
            "sensor_width": 18.7,
            "sensor_height": 18.7,
            "image_width": 3072,
            "image_height": 3072,
            "codec": "ARRIRAW",
            "is_anamorphic": True,
            "pixel_aspect": 2.0,
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "3K 1:1 was designed for shooting with 2x anamorphic lenses for a target deliverable of 2:1, fulfilling 4K mandates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "3K",
            "image_aspect": "1:1",
            "sensor_width": 18.7,
            "sensor_height": 18.7,
            "image_width": 3072,
            "image_height": 3072,
            "codec": "ProRes",
            "is_anamorphic": True,
            "pixel_aspect": 2.0,
            "manufacturer_notes": "3K 1:1 was designed for shooting with 2x anamorphic lenses for a target deliverable of 2:1, fulfilling 4K mandates.",
            "source": sources.get("Alexa 35 User Manual"),
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "3.8K",
            "image_aspect": "2:1",
            "format_name": "Ana. 2X",
            "sensor_width": 18.7,
            "sensor_height": 18.7,
            "image_width": 3840,
            "image_height": 1920,
            "codec": "ProRes",
            "is_anamorphic": True,
            "is_desqueezed": True,
            "pixel_aspect": 2.0,
            "source": sources.get("Alexa 35 User Manual"),
            "notes": "Dezqueezed from 3K 1:1",
            "manufacturer_notes": "3K 1:1 was designed for shooting with 2x anamorphic lenses for a target deliverable of 2:1, fulfilling 4K mandates.",
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "2.7K",
            "image_aspect": "8:9",
            "sensor_width": 16.7,
            "sensor_height": 18.8,
            "image_width": 2743,
            "image_height": 3086,
            "codec": "ARRIRAW",
            "is_anamorphic": True,
            "pixel_aspect": 2.0,
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "For projects shooting with 2x anamorphic lenses for a target deliverable of 16:9, fulfilling 4K mandates. Desqueeze applied in-camera.",
            "raw_recording_available": False,  # This is a rare case where the ARRI does not keep the raw data
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "UHD",
            "image_aspect": "16:9",
            "format_name": "Ana. 2X",
            "sensor_width": 16.7,
            "sensor_height": 18.8,
            "image_width": 3840,
            "image_height": 2160,
            "codec": "ProRes",
            "is_anamorphic": True,
            "is_desqueezed": True,
            "pixel_aspect": 2.0,
            "source": sources.get("Alexa 35 User Manual"),
            "notes": "Dezqueezed from 2.7K 8:9 | This is a rare case where the raw data is not kept, all processing happens in-camera",
            "manufacturer_notes": "For projects shooting with 2x anamorphic lenses for a target deliverable of 16:9, fulfilling 4K mandates. Desqueeze applied in-camera.",
            "raw_recording_available": False,  # This is a rare case where the ARRI does not keep the raw data
        },
        {
            "camera": cameras.get("Alexa 35") or Camera.objects.get("Alexa 35"),
            "image_format": "2K",
            "image_aspect": "16:9",
            "format_name": "S16",
            "sensor_width": 12.4,
            "sensor_height": 7.0,
            "image_width": 2048,
            "image_height": 1152,
            "codec": "ProRes",
            "source": sources.get("Alexa 35 User Manual"),
            "manufacturer_notes": "2K 16:9 S16 mimics the traditional Super 16 format for use with Super 16 lenses or as an in-camera center crop.",
        },
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
