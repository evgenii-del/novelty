from django.core.management.base import BaseCommand, CommandError
from blog.models import Rate
from blog.tasks import change_cours

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        change_cours()
