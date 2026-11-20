import os
from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a super admin if it does not exist yet."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin")
        parser.add_argument("--email", default="admin@example.com")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        if User.objects.filter(username=username).exists():
            msg = f"'{username}' already exists - skipped."
            self.stdout.write(self.style.WARNING(msg))
            return

        password = (os.environ.get("DJANGO_SUPERUSER_PASSWORD")
                    or self._ask_password())

        User.objects.create_superuser(
            username=username,
            email=options["email"],
            password=password,
        )
        msg = f"Super admin '{username}' created."
        self.stdout.write(self.style.SUCCESS(msg))

    def _ask_password(self):
        first = getpass("Password: ")
        if first != getpass("Password (again): "):
            raise CommandError("Passwords do not match.")
        if len(first) < 8:
            raise CommandError("Password must be at least 8 characters.")
        return first