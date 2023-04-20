import operator
from pathlib import Path
from functools import reduce

from django.conf import settings
from django.db.models import Q
from django.core.management.base import BaseCommand

from request.models import Request


class Command(BaseCommand):
    help = "Seed database with sample data."

    def handle(self, *args, **options):
        output = ""
        file = Path(settings.NGIX_DENY_CONFIGURATION_FILE)

        requests = Request.objects.filter(reduce(operator.or_, (Q(path__contains=x)
                                          for x in settings.DENY_IPS_WITH_PATHS)))

        with open(file, "r") as f:
            current = f.read()

        ips = set(r.ip for r in requests)
        for ip in ips:
            if not str(ip) in current:
                output += f"deny {ip};\n"

        with open(file, "a") as f:
            f.write(output)

        requests.delete()
