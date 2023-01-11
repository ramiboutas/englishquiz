

from django.core.management.base import BaseCommand
from socialmedia.tasks import share_random_question_as_poll



class Command(BaseCommand):
    help = "Shares a question as Poll to Social Media accounts."


    def handle(self, *args, **options):

        self.stdout.write("Sharing question as poll...")
        
        share_random_question_as_poll()

        self.stdout.write("Done.")

