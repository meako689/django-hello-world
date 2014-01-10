from django.core.management.base import BaseCommand
from django.db import models
import sys

class Command(BaseCommand):

    def handle(self, *args, **options):
        for model in models.get_models(include_deferred=True):
            msg= "{name}:{count}\n".format(
                    name=model.__name__,
                    count=model.objects.count()
            )
            sys.stdout.write(msg)
            sys.stderr.write('error:'+msg)

