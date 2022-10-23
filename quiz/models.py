from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

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
    (2, "2: Two text input"),
    (5, "5: One choice selection"),
    (6, "6: Multiple choice selection"),
)


class Quiz(models.Model):
    name = models.CharField(max_length=64)
    level = models.IntegerField(default=5, choices=QUIZ_LEVEL_CHOICES)
    slug = models.SlugField(blank=True, unique=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    image_credits_url = models.URLField(max_length=200, null=True)
    views = models.PositiveIntegerField(default=0)

    def get_detail_url(self):
        return reverse("quiz_detail", kwargs={"slug": self.slug, "level": self.level})

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("quiz_list")

    def add_view(self):
        self.views += 1
        self.save()

    def __str__(self):
        return f"{self.get_level_display()} - {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-views",)


class Lection(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField(blank=True)
    views = models.PositiveIntegerField(default=0)

    def get_first_question(self):
        return self.question_set.all().first()

    def get_absolute_url(self):
        return self.get_first_question().get_detail_url()

    def add_view(self):
        self.views += 1
        self.save()

    def __str__(self):
        return f"{self.name} ({self.quiz.name})"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("name",)


class Question(models.Model):
    lection = models.ForeignKey(Lection, on_delete=models.CASCADE)
    text_one = models.CharField(max_length=200, null=True, blank=True)
    text_two = models.CharField(max_length=200, null=True, blank=True)
    text_three = models.CharField(max_length=200, null=True, blank=True)
    type = models.PositiveSmallIntegerField(default=1, choices=QUESTION_TYPE_CHOICES)
    explanation = models.CharField(max_length=250, blank=True, null=True)
    promoted = models.BooleanField(default=False)

    @property
    def full_text(self):
        text = ""
        if self.type == 1:
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
        return reverse(
            "check_answer",
            kwargs={
                "slug_quiz": self.lection.quiz.slug,
                "level_quiz": self.lection.quiz.level,
                "slug_lection": self.lection.slug,
                "id_question": self.id,
            },
        )

    def update_progress_bar_url(self):
        return reverse(
            "update_progress_bar",
            kwargs={
                "slug_quiz": self.lection.quiz.slug,
                "level_quiz": self.lection.quiz.level,
                "slug_lection": self.lection.slug,
                "id_question": self.id,
            },
        )

    def get_translation_modal_url(self):  # not used, used Bootstrap Bundle JS instead
        return reverse("quiz_get_translation_modal", kwargs={"id_question": self.id})

    def remove_translation_modal_url(
        self,
    ):  # not used, used Bootstrap Bundle JS instead
        return reverse("quiz_remove_translation_modal", kwargs={"id_question": self.id})

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

    def __str__(self):
        return f"{self.lection.quiz.name} - {self.lection.name} - {self.text_one}"

    class Meta:
        ordering = ("id",)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DeeplLanguage(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    supports_formality = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-views"]

    def __str__(self) -> str:
        return self.name

    def add_view(self):
        self.views += 1
        self.save()


class TranslatedQuestion(models.Model):
    language = models.ForeignKey(DeeplLanguage, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    original_text = models.CharField(max_length=650)
    translated_text = models.CharField(max_length=650)

    created = models.DateField(auto_now_add=True, null=True)
    updated = models.DateField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.original_text
