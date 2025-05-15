from cameras.models import CameraManufacturer


def seed_manufacturers():
    manufacturers = [
        {"name": "Arri", "website": "https://www.arri.com/en"},
        {"name": "RED", "website": "https://www.red.com"},
    ]

    for mfg in manufacturers:
        CameraManufacturer.objects.get_or_create(**mfg)
