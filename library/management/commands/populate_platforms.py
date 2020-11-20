"""Populate platform"""
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from library.models import Platform
from scrapping import send_requests


class Command(BaseCommand):
    """Populate platforms command"""

    help = "Populate plaforms in db"

    def handle(self, *args, **options):  # pylint: disable=W0613
        """Handle command"""
        try:
            platforms_json = send_requests.get_platforms()

            platforms = []
            for platform in platforms_json:
                try:
                    platforms.append(
                        Platform(
                            name=platform.get("name"),
                            constructor=platform.get("company")["name"],
                            release_date=timezone.make_aware(
                                datetime.strptime(
                                    platform.get("release_date"), "%Y-%m-%d %H:%M:%S"
                                ),
                                timezone.get_current_timezone(),
                            ),
                        )
                    )
                except TypeError:
                    continue

            [platform.save() for platform in platforms]

        except Exception as error:
            raise CommandError(f"Error while populating platforms: {error}") from error

        self.stdout.write("Platforms populated", ending="")
