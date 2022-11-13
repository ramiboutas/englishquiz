from django_rich.management import RichCommand


class Command(RichCommand):
    def handle(self, *args, **options):
        # self.console.print("[bold red]Alert![/bold red]")
        # self.console.print("[italic red]Hello[/italic red] World!", locals())
        self.console.print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())