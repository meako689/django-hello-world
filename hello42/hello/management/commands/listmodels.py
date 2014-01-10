from django.core.management.base import BaseCommand, CommandError
from django.db import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        for model in models.get_models():
            print "{name}:{count}".format(
                    name=model.__name__,
                    count=model.objects.count()
            )

