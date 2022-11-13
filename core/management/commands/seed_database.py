import random

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction
from django.utils.text import slugify

from quiz.models import Answer
from quiz.models import Lection
from quiz.models import Question
from quiz.models import Quiz

# from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Seed database with sample data."

    @transaction.atomic
    def handle(self, *args, **options):
        if Quiz.objects.exists():
            raise CommandError(
                "This command cannot be run when any authors exist, to guard "
                + "against accidental use on production."
            )

        self.stdout.write("Seeding database...")

        # update_site()

        create_quiz_and_related_objects()

        self.stdout.write("Done.")


# def update_site():
#     domain = "localhost:8000"
#     Site.objects.filter(domain="example.com").update(domain=domain, name=domain)


def create_quiz_and_related_objects():
    lection_names = [f"Lection {i}" for i in range(1, 6)]
    question_names = [f"Question {i}" for i in range(1, 11)]

    def make_questions(lection, names):
        Question.objects.bulk_create(
            [
                Question(lection=lection, text_one=name, type=random.choice([1, 5]))
                for name in names
            ]
        )

    def make_lections(quiz, names):
        Lection.objects.bulk_create(
            [Lection(quiz=quiz, name=name, slug=slugify(name)) for name in names]
        )

    def make_answers(question):
        correct_answer = random.choice([1, 2, 3])

        if question.type == 5:
            answers = []
            for i in range(1, 4):
                answers.append(
                    Answer(
                        question=question,
                        name=f"Answer {i}",
                        correct=i == correct_answer,
                    )
                )
            Answer.objects.bulk_create(answers)

        elif question.type == 1:
            Answer.objects.create(
                question=question, name="The correct answer", correct=True
            )

    quiz = Quiz.objects.create(
        name="Phrasal verbs",
        level=5,
        image_url="https://picsum.photos/300/200",
        image_credits_url="https://picsum.photos/",
    )

    make_lections(quiz, lection_names)

    lections = Lection.objects.all()

    for lection in lections:
        make_questions(lection, question_names)
        questions = Question.objects.filter(lection=lection)
        for question in questions:
            make_answers(question)
