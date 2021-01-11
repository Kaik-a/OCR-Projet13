"""Populate platform"""
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from library.models import Platform
from scrapping import send_requests


class Command(BaseCommand):
    """Populate platforms command"""

    help = "Populate plaforms in db"

    def handle(self, *args, **options):  # pylint: disable=W0613
        """Handle command"""
        count = 0

        try:
            platforms_json = send_requests.get_platforms()

            platforms = []
            for platform in platforms_json:
                try:
                    platforms.append(
                        Platform(
                            name=platform.get("name"),
                        )
                    )
                except TypeError:
                    continue

            for platform in platforms:
                try:
                    platform.save()
                    count += 1
                except IntegrityError:
                    continue

        except Exception as error:
            raise CommandError(f"Error while populating platforms: {error}") from error

        self.stdout.write(f"Platforms populated - {count} platform(s)", ending="")
