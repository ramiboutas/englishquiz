from pathlib import Path

from django.conf import settings
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

NGIX_DENY_CONFIGURATION_FILE = "/etc/nginx/conf.d/deny.conf"


class Command(BaseCommand):
    help = "Seed database with sample data."

    def handle(self, *args, **options):
        output = ""
        file = Path(settings.NGIX_DENY_CONFIGURATION_FILE)
        requests = Request.objects.filter(path__in=settings.DENY_IPS_WITH_PATHS)
        with open(file, "r") as f:
            current = f.read()

        ips = set(r.ip for r in requests)
        for ip in ips:
            if not str(ip) in current:
                output += f"deny {ip};\n"

        with open(file, "a") as f:
            f.write(output)
