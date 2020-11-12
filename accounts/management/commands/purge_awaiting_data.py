"""Purge data above 24h"""
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from accounts.models import AwaitingData


class Command(BaseCommand):
    """Purge command"""
    help = "Delete awaiting data older than 24 hours"

    def handle(self, *args, **options):  # pylint: disable=W0613
        """Handle command"""
        try:
            AwaitingData.objects.filter(
                date__lte=datetime.now() - timedelta(hours=24)
            ).delete()
        except Exception as error:
            raise CommandError(
                f"Error while purging old awaiting data: {error}"
            ) from error

        self.stdout.write("Deleted awaiting datas older than 24 hours", ending="")
