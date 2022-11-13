from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from quiz.models import Quiz


class SeedDatabaseTests(TestCase):
    def call_command(self, *args, **kwargs):
        out = StringIO()
        err = StringIO()
        call_command(
            "seed_database",
            *args,
            stdout=out,
            stderr=err,
            **kwargs,
        )
        return out.getvalue(), err.getvalue()

    def test_error_data_exists(self):
        Quiz.objects.create(name="Testing quiz")

        msg = (
            "This command cannot be run when any authors exist, to guard "
            + "against accidental use on production."
        )

        with self.assertRaisesMessage(CommandError, msg):
            self.call_command()

    def test_success(self):
        out, err = self.call_command()

        self.assertEqual(out, "Seeding database...\nDone.\n")
        self.assertEqual(err, "")