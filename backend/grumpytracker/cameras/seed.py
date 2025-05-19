from cameras.models import CameraManufacturer, Camera, Format, Source
from django.db import transaction
from loguru import logger


@transaction.atomic
def clear_database():
    # Format.objects.delete() returns a tuple (count_deleted, dict_with_details)
    formats_deleted = Format.objects.all().delete()[0]
    sources_deleted = Source.objects.all().delete()[0]
    cameras_deleted = Camera.objects.all().delete()[0]
    manufacturers_deleted = CameraManufacturer.objects.all().delete()[0]

    logger.info(f"Deleted {manufacturers_deleted} manufacturers")
    logger.info(f"Deleted {cameras_deleted} cameras")
    logger.info(f"Deleted {sources_deleted} sources")
    logger.info(f"Deleted {formats_deleted} formats")

    return {
        "manufacturers": manufacturers_deleted,
        "cameras": cameras_deleted,
        "sources": sources_deleted,
        "formats": formats_deleted,
    }


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
        {
            "manufacturer": manufacturers.get("Arri")
            or CameraManufacturer.objects.get("Arri"),
            "model": "Alexa Mini LF",
            "sensor_type": "Large Format ARRI ALEV III (A2X) CMOS sensor with Bayer pattern color filter array",
            "max_filmback_width": 36.70,
            "max_filmback_height": 25.54,
            "max_image_width": 4448,
            "max_image_height": 3096,
            "min_frame_rate": 0.75,
            "max_frame_rate": 90,
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
            "file_name": "ARRI ALEXA 35 SUP 4.0.0 - User Manual.pdf",
        },
        {
            "name": "Alexa Mini User Manual",
            "url": "https://www.arri.com/resource/blob/347174/6b8fd84caac842b3c9292c910fcee693/alexa-mini-lf-sup-7-3-user-manual-data.pdf",
            "file_name": "ALEXA Mini LF SUP 7.3 - User Manual.pdf",
        },
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
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "4.5K LF",
            "image_aspect": "3:2",
            "format_name": "Open Gate",
            "sensor_width": 36.70,
            "sensor_height": 25.54,
            "image_width": 4448,
            "image_height": 3096,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa Mini User Manual"),
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "4.5K LF",
            "image_aspect": "2.39:1",
            "format_name": "Open Gate",
            "sensor_width": 36.70,
            "sensor_height": 15.31,
            "image_width": 4448,
            "image_height": 1856,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa Mini User Manual"),
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "3.8K LF",
            "image_aspect": "16:9",
            "format_name": "UHD",
            "sensor_width": 31.68,
            "sensor_height": 17.82,
            "image_width": 3840,
            "image_height": 2160,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa Mini User Manual"),
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "2.8K LF",
            "image_aspect": "1:1",
            "sensor_width": 23.76,
            "sensor_height": 23.76,
            "image_width": 2880,
            "image_height": 2880,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa Mini User Manual"),
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "3.4K",
            "image_aspect": "3.2",
            "format_name": "S35",
            "sensor_width": 28.25,
            "sensor_height": 18.16,
            "image_width": 3424,
            "image_height": 2202,
            "codec": "ARRIRAW",
            "source": sources.get("Alexa Mini User Manual"),
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "4.5K LF",
            "image_aspect": "3:2",
            "format_name": "Open Gate",
            "sensor_width": 36.70,
            "sensor_height": 25.54,
            "image_width": 4480,
            "image_height": 3096,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
            "manufacturer_notes": "This format adds 16px clip padding on left and right sides of frames. Sensor resolution is 4448x3096",
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "4.5K LF",
            "image_aspect": "2.39:1",
            "sensor_width": 36.70,
            "sensor_height": 15.31,
            "image_width": 4480,
            "image_height": 1856,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
            "manufacturer_notes": "This format adds 16px clip padding on left and right sides of frames. Sensor resolution is 4448x1856",
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "4.3K LF",
            "image_aspect": "16:9",
            "format_name": "UHD",
            "sensor_width": 35.64,
            "sensor_height": 20.05,
            "image_width": 3840,
            "image_height": 2160,
            "is_downsampled": True,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
            "notes": "This is a downsampled UHD format. Original sensor resolution was 4320×2430 pixels.",
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "4.3K LF",
            "image_aspect": "16:9",
            "format_name": "HD",
            "sensor_width": 35.64,
            "sensor_height": 20.05,
            "image_width": 1920,
            "image_height": 1080,
            "is_downsampled": True,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
            "notes": "This is a downsampled format. Original sensor resolution was 4320×2430 pixels.",
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "3.8K LF",
            "image_aspect": "16:9",
            "format_name": "UHD",
            "sensor_width": 31.68,
            "sensor_height": 17.82,
            "image_width": 3840,
            "image_height": 2160,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "3.8K LF",
            "image_aspect": "16:9",
            "format_name": "2K",
            "sensor_width": 31.68,
            "sensor_height": 17.82,
            "image_width": 2048,
            "image_height": 1152,
            "is_downsampled": True,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
            "notes": "This is a downsampled format. Original sensor resolution was 3840x2160 pixels.",
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "3.8K LF",
            "image_aspect": "16:9",
            "format_name": "HD",
            "sensor_width": 31.68,
            "sensor_height": 17.82,
            "image_width": 1920,
            "image_height": 1080,
            "is_downsampled": True,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
            "notes": "This is a downsampled format. Original sensor resolution was 3840x2160 pixels.",
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "2.8K LF",
            "image_aspect": "1:1",
            "sensor_width": 23.76,
            "sensor_height": 26.76,
            "image_width": 3072,
            "image_height": 3024,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
            "manufacturer_notes": "This format adds 96 px clip padding on left and right sides of frames and 72px padding on top and bottom. Sensor resolution is 2880x2880",
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "3.2K LF",
            "image_aspect": "16:9",
            "format_name": "S35",
            "sensor_width": 26.40,
            "sensor_height": 14.85,
            "image_width": 3200,
            "image_height": 1800,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "2.8K",
            "image_aspect": "4:3",
            "format_name": "S35",
            "sensor_width": 23.76,
            "sensor_height": 17.81,
            "image_width": 2880,
            "image_height": 2160,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
        },
        {
            "camera": cameras.get("Alexa Mini LF")
            or Camera.objects.get("Alexa Mini LF"),
            "image_format": "2.8K",
            "image_aspect": "4:3",
            "format_name": "HD",
            "sensor_width": 23.76,
            "sensor_height": 13.36,
            "image_width": 1920,
            "image_height": 1080,
            "is_downsampled": True,
            "codec": "ProRes",
            "source": sources.get("Alexa Mini User Manual"),
            "notes": "This is a downsampled format. Original sensor resolution was 2880x1620 pixels.",
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
