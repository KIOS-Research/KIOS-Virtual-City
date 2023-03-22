from django.core.management.base import BaseCommand
from basp.views import testfunction

class Command(BaseCommand):
    help="asdffgsddf"

    def handle(self, *args, **kwargs):
        testfunction()