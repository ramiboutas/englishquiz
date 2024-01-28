from __future__ import annotations

import random

import auto_prefetch
from django_linkedin_posts.models import Poll as LiPoll
from django_linkedin_posts.models import Post as LiPost

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


from utils.telegram import report_to_admin


QUIZ_LEVEL_CHOICES = (
    (1, "A1"),
    (2, "A2"),
    (3, "B1"),
    (4, "B2"),
    (5, "C1"),
    (6, "C2"),
)

QUESTION_TYPE_CHOICES = (
    (1, "1: One text input"),
    (2, "2: Two text inputs"),
    (5, "5: One choice selection"),
)


class Quiz(models.Model):
    name = models.CharField(max_length=64)
    level = models.IntegerField(default=5, choices=QUIZ_LEVEL_CHOICES)
    slug = models.SlugField(blank=True, unique=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    image_credits_url = models.URLField(max_length=200, null=True)

    def get_detail_url(self):
        return reverse("quiz_detail", kwargs={"slug": self.slug, "level": self.level})

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("quiz_list")

    def __str__(self):
        return f"{self.get_level_display()} - {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Lection(auto_prefetch.Model):
    quiz = auto_prefetch.ForeignKey(Quiz, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField(blank=True)

    def get_first_question(self):
        return self.question_set.all().first()

    def get_absolute_url(self):
        return self.get_first_question().get_detail_url()

    def __str__(self):
        return f"{self.name} ({self.quiz.name})"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("name",)


class Question(auto_prefetch.Model):
    lection = auto_prefetch.ForeignKey(Lection, on_delete=models.CASCADE)
    text_one = models.CharField(max_length=200, null=True, blank=True)
    text_two = models.CharField(max_length=200, null=True, blank=True)
    text_three = models.CharField(max_length=200, null=True, blank=True)
    type = models.PositiveSmallIntegerField(default=5, choices=QUESTION_TYPE_CHOICES)
    explanation = models.TextField(max_length=250, blank=True, null=True)
    promoted = models.BooleanField(default=False)

    linkedin_poll = auto_prefetch.OneToOneField(
        LiPoll,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    linkedin_poll_commented = models.BooleanField(default=False, editable=False)

    linkedin_post = auto_prefetch.OneToOneField(
        LiPost,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    linkedin_post_commented = models.BooleanField(default=False, editable=False)

    created_by = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    @property
    def full_text(self):
        text = ""
        if self.type == 1 or self.type == 2:
            text += f"{self.text_one} ____ {self.text_two}"
            if self.text_three:
                text += f" ____ {self.text_three}"

        if self.type == 5:
            text += f"{self.text_one}"
            if self.text_two:
                text += f"\n {self.text_two}"
            if self.text_three:
                text += f"\n {self.text_three}"
        return text

    def progress_percentage(self, extra=0):
        lection_questions = list(Question.objects.filter(lection=self.lection))
        index = lection_questions.index(self) + extra
        progress_percentage = int(index * 100 / len(lection_questions))
        return progress_percentage

    def get_answer_list(self):
        # for polls
        return [a.name for a in self.answer_set.all()]

    def get_correct_answer_order(self):
        # for polls
        for index, a in enumerate(self.answer_set.all()):
            if a.correct:
                return index

    def get_detail_url(self):
        return reverse(
            "question_detail",
            kwargs={
                "slug_quiz": self.lection.quiz.slug,
                "level_quiz": self.lection.quiz.level,
                "slug_lection": self.lection.slug,
                "id_question": self.id,
            },
        )

    def get_absolute_url(self):
        return self.get_detail_url()

    def check_answer_url(self):
        return reverse("quiz_check_answer", kwargs={"id_question": self.id})

    def update_progress_bar_url(self):
        return reverse("quiz_update_progress_bar", kwargs={"id_question": self.id})

    def is_first(self):
        return self.__class__.objects.filter(lection=self.lection).first() == self

    def is_last(self):
        return self.__class__.objects.filter(lection=self.lection).last() == self

    def previous_object(self):
        return (
            self.__class__.objects.filter(id__lt=self.id, lection=self.lection)
            .order_by("id")
            .last()
        )

    def next_object(self):
        return (
            self.__class__.objects.filter(id__gt=self.id, lection=self.lection)
            .order_by("id")
            .first()
        )

    def _get_question_text(self):
        """
        It generates text from a Question instance
        """
        text = ""
        if self.type == 1 or self.type == 2:
            text += (
                "What do you think that comes in the gap of the next sentence? 🤔\n\n"
            )
            text += f"📚 {self.text_one} ____ {self.text_two}"
            if self.text_three:
                text += f" ____ {self.text_three}\n"
        if self.type == 5:
            text += "Which option fits better in the gap of the next sentence? 🤔\n\n"
            text += f"📚 {self.text_one}\n"
            if self.text_two:
                text += f"📚 {self.text_two}\n"
            if self.text_three:
                text += f"📚 {self.text_three}\n"
            text += "\n💡 Options:\n"
            for answer in self.answer_set.all():
                text += f" 🔹 {answer.name}\n"

        return text

    def get_question_promotion_text(self, add_link=True):
        """
        It generates text from a question instance
        """
        question_text = self._get_question_text()

        # Producing text
        text = f"Here a small question for you!\n\n"
        text += f"{question_text} \n\n"
        if add_link:
            text += "Check out the right answer here:\n"
            text += f"👉 {settings.SITE_BASE_URL}{self.get_detail_url()} \n\n"

        return text

    def get_poll_explanation_text(self, add_link=True):
        text_options = [
            "Guess the answer!",
            "What do you think the answer is?",
            "What goes in the gap?",
        ]
        text = random.choice(text_options)
        if add_link:
            text += "\n\nCheck the right answer here 👉 "
            text += f"{settings.SITE_BASE_URL}{self.get_detail_url()}"

        return text

    def post_comment_with_right_answer(self):
        if self.type == 5:
            right = self.answer_set.filter(correct=True)[0]
            text = f"The right answer was: {right.name}\n\n"
            text += f"Learn more 👉{settings.SITE_BASE_URL}{self.get_detail_url()}"
            return text

        text = "Check the right answer here 👉 "
        text += f"{settings.SITE_BASE_URL}{self.get_detail_url()}"
        return text

    def __str__(self):
        return f"{self.lection.quiz.name} - {self.lection.name} - {self.text_one}"

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("id",)


class Answer(auto_prefetch.Model):
    question = auto_prefetch.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DeeplLanguage(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    supports_formality = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class TranslatedQuestion(auto_prefetch.Model):
    language = auto_prefetch.ForeignKey(DeeplLanguage, on_delete=models.CASCADE)
    question = auto_prefetch.ForeignKey(Question, on_delete=models.CASCADE)
    original_text = models.CharField(max_length=650)
    translated_text = models.CharField(max_length=650)
    created = models.DateField(auto_now_add=True, null=True)
    updated = models.DateField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.original_text
