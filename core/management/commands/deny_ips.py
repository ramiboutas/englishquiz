from django.core.management.base import BaseCommand

from request.models import Request


DENY_IPS_WITH_PATHS = [
    "/wp-login.php",
    "/.env",
    "//wp1/wp-includes/wlwmanifest.xml",
    "//2019/wp-includes/wlwmanifest.xml",
    "//web/wp-includes/wlwmanifest.xml",
    "//wp/wp-includes/wlwmanifest.xml",
    "//site/wp-includes/wlwmanifest.xml",
]


class Command(BaseCommand):
    help = "Seed database with sample data."

    def handle(self, *args, **options):
        requests = Request.objects.filter(path__in=DENY_IPS_WITH_PATHS)
        output = ""
        for request in requests:
            output += f"deny {request.ip};\n"
        self.stdout.write(output)
