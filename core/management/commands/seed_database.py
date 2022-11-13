import random
# from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from quiz.models import Quiz, Lection, Question, Answer


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
            [Question(lection=lection, text_one=name, type=5) for name in names]
        )

    def make_lections(quiz, names):
        lections = Lection.objects.bulk_create(
            [Lection(quiz=quiz, name=name, slug=slugify(name)) for name in names]
        )
    
    def make_answers(question):
        correct_answer = random.choice([1, 2, 3])
        answers = []
        for i in range(1,4):
            answers.append(Answer(
                question=question,
                name=f"Answer {i}",
                correct=i==correct_answer
                )
            )
        Answer.objects.bulk_create(answers)

    quiz = Quiz.objects.create(
        name = "Phrasal verbs",
        level = 5,
        image_url="https://picsum.photos/300/200",
        image_credits_url="https://picsum.photos/",
    )
    
    make_lections(quiz, lection_names)

    qs_lections = Lection.objects.all()

    for lection in qs_lections:            
        make_questions(lection, question_names)

        qs_questions = Question.objects.filter(lection=lection)
        for question in qs_questions:
            make_answers(question)
    

