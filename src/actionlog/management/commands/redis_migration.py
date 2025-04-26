from django.core.management.base import BaseCommand
from redis_om import Migrator


class Command(BaseCommand):
    help = "Runs redis migrations"  # noqa

    def handle(self, *args: tuple, **options: dict) -> None:
        Migrator().run()
