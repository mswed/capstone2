from users.models import User
from cameras.models import Format
from django.db import transaction
from loguru import logger


@transaction.atomic
def clear_database():
    # Format.objects.delete() returns a tuple (count_deleted, dict_with_details)
    users_deleted = User.objects.all().delete()[0]

    logger.info(f"Deleted {users_deleted} users")

    return {
        "users": users_deleted,
    }


@transaction.atomic
def seed_users():
    users = [
        {
            "username": "wilsonpuddnhdead",
            "first_name": "Moshe",
            "last_name": "Swed",
            "email": "mswed@beapot.com",
            "role": "Tracking Supervisor",
            "studio": "Powerhouse VFX",
        },
    ]

    created_users = {}
    for u in users:
        user, new = User.objects.get_or_create(**u)
        format_obj = Format.objects.get(id=1)
        user.favorite_formats.add(format_obj)
        created_users[u["username"]] = user
        logger.info(f"{'Created' if new else 'Found'} user: {user.username}")

    return created_users


def seed_db():
    clear_database()
    users = seed_users()
