from django.core.management.base import BaseCommand
from projects.seed import seed_db, clear_database


class Command(BaseCommand):
    help = "Seed project database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true", help="Clear database before seeding"
        )

    def handle(self, *args, **options):
        if options["reset"]:
            clear_database()
            self.stdout.write("Clearing and reseeding database...")
        else:
            self.stdout.write("Seeding database...")

        seed_db()

        self.stdout.write(self.style.SUCCESS("Successfully seeded camera database"))
